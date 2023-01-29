from typing import Tuple
import logging
import os
import socket
import time
from django.forms.models import model_to_dict

from web.models import OverwatchService, OverwatchLog

logger = logging.getLogger(__name__)


def run():
    logger.info("Run overwatch job")

    # Check the availability of all configured TCP servers
    i = 0
    while os.getenv(f"OW_TCP_{i}", None):
        tcp_server_availability(os.getenv(f"OW_TCP_{i}"))
        i += 1


def tcp_server_availability(config):
    name, host, port = _parse_config(config)
    if not port:
        logger.error(f"Port is not defined for TCP server {name}")
        return
    logger.debug(f"Check if TCP server on host {host} and port {port} is available")

    # Check if there is already an DB entry for this overwatch job
    if OverwatchService.objects.filter(name=name).exists():
        service = OverwatchService.objects.get(name=name)
        service.host = host
        service.port = port
    else:
        service = OverwatchService(
            name=name, type="tcp", host=host, port=port, available=False, notified=False
        )

    try:
        time.sleep(2)
        start = time.time_ns()
        sock = socket.create_connection((host, port), timeout=5)
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


def _parse_config(config: str) -> Tuple[str, str, int]:
    config = config.split(",")
    name = config[0]
    host = config[1]
    port = None
    if len(config) == 3:
        port = int(config[2])
    return name, host, port


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
    rows = []
    for service in OverwatchService.objects.order_by("type").all():
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
        rows.append(model_as_dict)

    context = {
        "ow_services_header": ["Name", "Type", "Available", "Up-Time", "Last Updated"],
        "ow_services": rows,
    }
    return context
