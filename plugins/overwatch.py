from typing import Tuple
import logging
import operator
import functools
import os
import socket
import time
import subprocess
import requests
from django.forms.models import model_to_dict
from django.db.models import Q

from web.models import OverwatchService, OverwatchLog

logger = logging.getLogger(__name__)


def run():
    logger.info("Run overwatch job")

    # Check the availability of all configured TCP servers
    i = 0
    while os.getenv(f"OW_TCP_{i}", None):
        tcp_server_availability(os.getenv(f"OW_TCP_{i}"))
        i += 1

    # Check the availability of all configured HTTP servers
    i = 0
    while os.getenv(f"OW_HTTP_{i}", None):
        http_server_availability(os.getenv(f"OW_HTTP_{i}"))
        i += 1

    # Check the availability of all configured ping hosts
    i = 0
    while os.getenv(f"OW_PING_{i}", None):
        ping_availability(os.getenv(f"OW_PING_{i}"))
        i += 1

    # Delete services without a corresponding environment variable from database
    if os.getenv("OW_REMOVE_OLD_SERVICES", "True") == "True":
        clean_database()


def get_service(config: str, type: str) -> OverwatchService:
    name, host, port = _parse_config(config)
    if OverwatchService.objects.filter(name=name, type=type).exists():
        service = OverwatchService.objects.get(name=name, type=type)
        service.host = host
        service.port = port
        return service
    else:
        return OverwatchService(
            name=name, type=type, host=host, port=port, available=False
        )


def tcp_server_availability(config):
    service = get_service(config, "tcp")
    if not service.port:
        logger.error(f"Port is not defined for TCP server {service.name}")
        return
    logger.debug(
        f"Check if TCP server on host {service.host} and port {service.port} is available"
    )

    try:
        time.sleep(2)
        start = time.time_ns()
        sock = socket.create_connection((service.host, service.port), timeout=5)
        time_ms = (time.time_ns() - start) / 1000000
        logger.debug(f"Time to connect to TCP server: {time_ms}ms")
        sock.shutdown(socket.SHUT_RDWR)
        sock.close()
        service.available = True
        service.notified = False
    except socket.error as e:
        time_ms = 0
        service.available = False

    service.save()

    OverwatchLog(service=service, latency=time_ms).save()


def http_server_availability(config):
    service = get_service(config, "http")

    try:
        # Don't verify SSL certificate because we only check for availability
        response = requests.get(service.host, timeout=5, verify=False, allow_redirects=False)
        time_ms = response.elapsed.total_seconds() * 1000
        logger.debug(f"Time to connect to HTTP server: {time_ms}ms")
        if response.status_code < 400:
            service.available = True
            service.notified = False
        else:
            time_ms = 0
            service.available = False
    except requests.exceptions.RequestException as e:
        time_ms = 0
        service.available = False

    service.save()

    OverwatchLog(service=service, latency=time_ms).save()


def ping_availability(config: str):
    service = get_service(config, "ping")
    logger.debug(f"Check if host {service.host} is available via ping")

    result = subprocess.Popen(
        ["/usr/bin/ping", "-c", "4", service.host], stdout=subprocess.PIPE
    )
    result.wait()
    time_ms = 0
    if result.returncode == 0:
        service.available = True
        service.notified = False
        output = result.stdout.readlines()[-1].decode("utf-8").split("/")
        if len(output) >= 5:
            avg = output[4]
            time_ms = float(avg)
    else:
        service.available = False

    service.save()

    OverwatchLog(service=service, latency=time_ms).save()


def _parse_config(config: str) -> Tuple[str, str, int]:
    config = config.split(",")
    name = config[0]
    host = config[1]
    port = 0
    if len(config) == 3:
        port = int(config[2])
    return name, host, port


def clean_database():
    db_entries = []
    i = 0
    while os.getenv(f"OW_TCP_{i}", None):
        name, _, _ = _parse_config(os.getenv(f"OW_TCP_{i}"))
        db_entries.append((name, "tcp"))
        i += 1
    i = 0
    while os.getenv(f"OW_HTTP_{i}", None):
        name, _, _ = _parse_config(os.getenv(f"OW_HTTP_{i}"))
        db_entries.append((name, "http"))
        i += 1
    i = 0
    while os.getenv(f"OW_PING_{i}", None):
        name, _, _ = _parse_config(os.getenv(f"OW_PING_{i}"))
        db_entries.append((name, "ping"))
        i += 1

    query = functools.reduce(
        operator.or_,
        (Q(name=name, type=type) for name, type in db_entries),
    )

    OverwatchService.objects.exclude(query).delete()


def is_configured() -> bool:
    ping = os.getenv("OW_PING_0", None)
    tcp = os.getenv("OW_TCP_0", None)
    http = os.getenv("OW_HTTP_0", None)
    if ping or tcp or http:
        return True
    return False


def sent_notifications() -> bool:
    notify = False
    for service in OverwatchService.objects.all():
        if not service.available and not service.notified:
            notify = True
            service.notified = True
            service.save()
    return notify


def get_data_as_table():
    tcp_services = []
    http_services = []
    ping_services = []
    for service in OverwatchService.objects.all():
        up = (
            OverwatchLog.objects.filter(service=service)
            .exclude(latency__exact=0.0)
            .count()
        )
        number = OverwatchLog.objects.filter(service=service).count()
        up_time = up / number
        model_as_dict = model_to_dict(service)
        model_as_dict["up_time"] = f"{int(up_time * 100)}%"
        model_as_dict["modification_time"] = service.modification_time
        if service.type == "tcp":
            tcp_services.append(model_as_dict)
        elif service.type == "http":
            http_services.append(model_as_dict)
        elif service.type == "ping":
            ping_services.append(model_as_dict)

    context = {
        "ow_services_header": ["Name", "Available", "Up-Time", "Last Updated"],
        "ow_tcp_services": tcp_services,
        "ow_http_services": http_services,
        "ow_ping_services": ping_services,
    }
    return context
