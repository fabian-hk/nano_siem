from typing import Tuple
import shutil
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

from web.models import NetworkService, NetworkServiceLog, DiskService, DiskServiceLog

logger = logging.getLogger(__name__)


def run():
    logger.info("Run overwatch job")

    # Check the availability of all configured disk services
    i = 0
    while os.getenv(f"OW_DISK_{i}", None):
        disk_availability(os.getenv(f"OW_DISK_{i}"))
        i += 1

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


def get_network_service(config: str, type: str) -> NetworkService:
    name, host, port = _parse_config(config)
    if NetworkService.objects.filter(name=name, type=type).exists():
        service = NetworkService.objects.get(name=name, type=type)
        service.host = host
        service.port = port
        return service
    else:
        return NetworkService(
            name=name, type=type, host=host, port=port, available=False
        )


def tcp_server_availability(config):
    service = get_network_service(config, "tcp")
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

    NetworkServiceLog(service=service, latency=time_ms).save()


def http_server_availability(config):
    service = get_network_service(config, "http")

    try:
        response = requests.get(
            service.host,
            timeout=5,
            verify=(os.getenv("OW_HTTP_VERIFY_SSL", "True") == "True"),
            allow_redirects=False,
        )
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

    NetworkServiceLog(service=service, latency=time_ms).save()


def ping_availability(config: str):
    service = get_network_service(config, "ping")
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

    NetworkServiceLog(service=service, latency=time_ms).save()


def get_disk_service(config: str) -> DiskService:
    config_split = config.split(",")
    if len(config_split) > 2:
        name = config_split[0]
        device = config_split[1]
        mount_point = config_split[2]
        uuid = None
        if len(config_split) > 3:
            uuid = config_split[3]
        if DiskService.objects.filter(name=name, type="disk").exists():
            service = DiskService.objects.get(name=name, type="disk")
            service.device = device
            service.mount_point = mount_point
            service.uuid = uuid
            return service
        else:
            return DiskService(
                name=name,
                type="disk",
                device=device,
                mount_point=mount_point,
                uuid=uuid,
            )
    else:
        logger.error(f"Invalid overwatch disk configuration: {config}")
        return None


def disk_availability(config: str):
    path_prefix = os.getenv("OW_DISK_ROOTFS_PREFIX", "/mnt/rootfs")
    service = get_disk_service(config)
    if not service:
        return
    logger.debug(f"Check if disk {service.name} is available")

    available = False
    with open(f"{path_prefix}/proc/mounts", "r") as f:
        for line in f:
            parts = line.split(" ")
            if (
                parts[0] == service.device
                and parts[1] == path_prefix + service.mount_point
            ):
                logger.debug(f"Disk {parts[0]} is mounted at {parts[1]}")
                available = True
                break

    if service.uuid:
        try:
            symlink = os.readlink(f"{path_prefix}/dev/disk/by-uuid/{service.uuid}")
            if symlink.split("/")[-1] == service.device.split("/")[-1]:
                logger.debug(
                    f"Disk with UUID {service.uuid} has the correct device name /dev/{symlink.split('/')[-1]}"
                )
                available &= True
            else:
                available = False
        except FileNotFoundError as e:
            available = False

    service.available = available
    if available:
        service.notified = False

    service.save()

    usage_free = 0
    usage_used = 0
    if available:
        disk_usage = shutil.disk_usage(
            (path_prefix + service.mount_point)
            .encode("latin1")
            .decode("unicode_escape")
        )
        logger.debug(f"Usage of {service.mount_point}: {disk_usage}")
        usage_free = disk_usage.free
        usage_used = disk_usage.used

    DiskServiceLog(
        service=service,
        available=available,
        free_space=usage_free,
        used_space=usage_used,
    ).save()


def _parse_config(config: str) -> Tuple[str, str, int]:
    config = config.split(",")
    name = config[0]
    host = config[1]
    port = 0
    if len(config) == 3:
        port = int(config[2])
    return name, host, port


def clean_database():
    # Clean network services by collecting all existing services
    # and removing all services that are not in the list anymore.
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

    NetworkService.objects.exclude(query).delete()

    # Clean up the disk services in the same way
    db_entries = []
    i = 0
    while os.getenv(f"OW_DISK_{i}", None):
        name = os.getenv(f"OW_DISK_{i}").split(",")[0]
        db_entries.append((name, "disk"))
        i += 1

    query = functools.reduce(
        operator.or_,
        (Q(name=name, type=type) for name, type in db_entries),
    )

    DiskService.objects.exclude(query).delete()


def is_configured() -> bool:
    ping = os.getenv("OW_PING_0", None)
    tcp = os.getenv("OW_TCP_0", None)
    http = os.getenv("OW_HTTP_0", None)
    if ping or tcp or http:
        return True
    return False


def sent_notifications() -> bool:
    notify = False
    for service in NetworkService.objects.all():
        if not service.available and not service.notified:
            notify = True
            service.notified = True
            service.save()

    for service in DiskService.objects.all():
        if not service.available and not service.notified:
            notify = True
            service.notified = True
            service.save()

    return notify


def get_data_as_table():
    tcp_services = []
    http_services = []
    ping_services = []
    for service in NetworkService.objects.all():
        up = (
            NetworkServiceLog.objects.filter(service=service)
            .exclude(latency__exact=0.0)
            .count()
        )
        number = NetworkServiceLog.objects.filter(service=service).count()
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

    disk_services = []
    for service in DiskService.objects.all():
        up = DiskServiceLog.objects.filter(service=service, available=True).count()
        number = DiskServiceLog.objects.filter(service=service).count()
        up_time = up / number
        model_as_dict = model_to_dict(service)
        model_as_dict["up_time"] = f"{int(up_time * 100)}%"
        model_as_dict["modification_time"] = service.modification_time
        try:
            last_log = (
                DiskServiceLog.objects.filter(service=service)
                .exclude(free_space=0, used_space=0)
                .latest("timestamp")
            )
            model_as_dict[
                "details"
            ] = f"{last_log.used_space / (last_log.free_space + last_log.used_space) * 100:.2f}% used"
        except DiskServiceLog.DoesNotExist:
            model_as_dict["details"] = "- used"
        disk_services.append(model_as_dict)

    context = {
        "ow_services_header": ["Name", "Available", "Up-Time", "Last Updated"],
        "ow_tcp_services": tcp_services,
        "ow_http_services": http_services,
        "ow_ping_services": ping_services,
        "ow_disk_services": disk_services,
    }
    return context
