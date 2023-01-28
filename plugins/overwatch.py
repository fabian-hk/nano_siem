import logging
import os
import socket
import time

from web.models import OverwatchService, OverwatchLog

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def run():
    logger.info("Run overwatch job")
    i = 0
    while os.getenv(f"OW_TCP_{i}", None):
        tcp_server_availability(os.getenv(f"OW_TCP_{i}"))
        i += 1


def tcp_server_availability(config):
    config = config.split(",")
    name = config[0]
    host = config[1]
    port = config[2]
    logger.debug(f"Check if TCP server on host {host} and port {port} is available")

    # Check if there is already an DB entry for this overwatch job
    if OverwatchService.objects.filter(name=name).exists():
        service = OverwatchService.objects.get(name=name)
    else:
        service = OverwatchService(
            name=name,
            type="tcp",
            available=False
        )
    available = False
    try:
        time.sleep(2)
        start = time.time_ns()
        sock = socket.create_connection((host, port), timeout=5)
        time_ms = (time.time_ns() - start) / 1000000
        logger.debug(f"Time to connect to TCP server: {time_ms}ms")
        sock.shutdown(socket.SHUT_RDWR)
        sock.close()
        available = True
    except socket.error as e:
        time_ms = 0
    service.available = available
    service.save()

    OverwatchLog(service=service, latency=time_ms).save()


def is_configured() -> bool:
    ping = os.getenv("OW_PING_0", None)
    tcp = os.getenv("OW_TCP_0", None)
    http = os.getenv("OW_HTTP_0", None)
    if ping or tcp or http:
        return True
    return False


if __name__ == "__main__":
    run()
