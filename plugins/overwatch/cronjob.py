from typing import Tuple
from threading import Thread
import shutil
import logging
import operator
import functools
import os
import socket
import time
import subprocess
import requests
from django.db.models import Q

from plugins.overwatch.models import (
    NetworkService,
    NetworkServiceLog,
    DiskService,
    DiskServiceLog,
)

logger = logging.getLogger(__name__)


def run():
    # Only run if the required configuration is present
    if not is_configured():
        return

    logger.info("Run overwatch job")

    threads = []
    i = 0
    while os.getenv(f"OVERWATCH_{i}", None):
        name, type = _parse_config(os.getenv(f"OVERWATCH_{i}"))
        if type == "disk":
            threads.append(
                Thread(target=disk_availability, args=(os.getenv(f"OVERWATCH_{i}"),))
            )
        elif type == "tcp":
            threads.append(
                Thread(
                    target=tcp_server_availability, args=(os.getenv(f"OVERWATCH_{i}"),)
                )
            )
        elif type == "http":
            threads.append(
                Thread(
                    target=http_server_availability, args=(os.getenv(f"OVERWATCH_{i}"),)
                )
            )
        elif type == "ping":
            threads.append(
                Thread(target=ping_availability, args=(os.getenv(f"OVERWATCH_{i}"),))
            )
        i += 1

    # Start all threads
    for t in threads:
        t.start()

    # Delete services without a corresponding environment variable from database
    if os.getenv("OW_REMOVE_OLD_SERVICES", "True") == "True":
        clean_database()

    # Wait for all threads to finish
    for t in threads:
        t.join()


def get_network_service(config: str, type: str) -> NetworkService:
    config_split = config.split(",")
    name = config_split[0]
    host = config_split[2]
    port = config_split[3] if len(config_split) > 3 else 0

    if NetworkService.objects.filter(name=name, type=type).exists():
        service = NetworkService.objects.get(name=name, type=type)
        service.host = host
        service.port = port
        return service
    else:
        return NetworkService(name=name, type=type, host=host, port=port)


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
        sock = socket.create_connection(
            (service.host, service.port),
            timeout=int(os.getenv("OW_NETWORK_TIMEOUT", "30")),
        )
        time_ms = (time.time_ns() - start) / 1000000
        logger.debug(f"Time to connect to TCP server: {time_ms}ms")
        sock.shutdown(socket.SHUT_RDWR)
        sock.close()
        service.available()
    except socket.error as e:
        time_ms = 0
        service.unavailable()

    NetworkServiceLog(service=service, latency=time_ms).save()


def http_server_availability(config):
    service = get_network_service(config, "http")

    try:
        response = requests.get(
            service.host,
            timeout=int(os.getenv("OW_NETWORK_TIMEOUT", "30")),
            verify=(os.getenv("OW_HTTP_VERIFY_SSL", "True") == "True"),
            allow_redirects=False,
        )
        time_ms = response.elapsed.total_seconds() * 1000
        logger.debug(f"Time to connect to HTTP server: {time_ms}ms")
        if response.status_code < 400:
            service.available()
        else:
            time_ms = 0
            service.unavailable()
    except requests.exceptions.RequestException as e:
        time_ms = 0
        service.unavailable()

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
        service.available()
        output = result.stdout.readlines()[-1].decode("utf-8").split("/")
        if len(output) >= 5:
            avg = output[4]
            time_ms = float(avg)
    else:
        service.unavailable()

    NetworkServiceLog(service=service, latency=time_ms).save()


def get_disk_service(config: str) -> DiskService | None:
    config_split = config.split(",")
    if len(config_split) > 2:
        name = config_split[0]
        device = config_split[2]
        mount_point = config_split[3]
        uuid = None
        if len(config_split) > 4:
            uuid = config_split[4]
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

    if available:
        service.available()
    else:
        service.unavailable()

    usage_free = 0
    usage_used = 0
    if available:
        # Encode the mount_path in this way to avoid problems with backslashes
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


def _parse_config(config: str) -> Tuple[str, str]:
    config = config.split(",")
    name = config[0]
    type = config[1]
    return name, type


def clean_database():
    # Clean service tables by collecting all existing services
    # and removing all services that are not in the list anymore.
    network_services = []
    disk_services = []
    i = 0
    while os.getenv(f"OVERWATCH_{i}", None):
        name, type = _parse_config(os.getenv(f"OVERWATCH_{i}"))
        if type == "disk":
            disk_services.append((name, type))
        else:
            network_services.append((name, type))
        i += 1

    if network_services:
        # Build query with OR operation to keep all existing services
        query = functools.reduce(
            operator.or_,
            (Q(name=name, type=type) for name, type in network_services),
        )

        # Delete all services except for the existing ones
        NetworkService.objects.exclude(query).delete()
    else:
        NetworkService.objects.all().delete()

    if disk_services:
        query = functools.reduce(
            operator.or_,
            (Q(name=name, type=type) for name, type in disk_services),
        )

        DiskService.objects.exclude(query).delete()
    else:
        DiskService.objects.all().delete()


def is_configured() -> bool:
    if os.getenv("OVERWATCH_0", None):
        return True
    return False
