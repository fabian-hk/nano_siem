from pathlib import Path

import os
import django
import shlex
from datetime import datetime
import logging

import random

# LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
# logging.basicConfig(level=LOG_LEVEL, format="%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

# Prepare Django framework to make database transaction
#os.environ["DJANGO_SETTINGS_MODULE"] = "nano_siem.settings"
#django.setup()

logger = logging.getLogger(__name__)
#logger.setLevel(logging.DEBUG)

from web.models import Service, ServiceLog
from plugins.utils import str_to_int

log_file = Path(os.getenv("TRAEFIK_SERVICE_LOG_PATH"))
name = os.getenv('TRAEFIK_SERVICE_NAME', "Traefik")


def setup():
    service = Service(name="Traefik", type="traefik", log_position=0, log_path=str(log_file.resolve()))
    service.save()


def run():
    logger.info(f"Start logging for {name} job")
    service = Service.objects.get(name=name)
    with log_file.open("rt") as f:
        i = 0
        for i, line in enumerate(f):
            if i > service.log_position:
                data = shlex.split(line.rstrip("\n"))
                ip = data[0]
                raw_data = f"{data[3].lstrip('[')} {data[4].rstrip(']')}"
                timestamp = datetime.strptime(raw_data, "%d/%b/%Y:%H:%M:%S %z")
                requested_service = data[11]
                user = data[2]
                event_request_method = data[5].split(" ")
                event = event_request_method[1]
                request_method = event_request_method[0]
                user_agent = data[9]
                http_status = str_to_int(data[6])
                content_size = str_to_int(data[7])
                longitude = 65.01236 + random.randint(-40, 40)
                latitude = 25.46816 + random.randint(-40, 40)
                country_name = "Finland"
                city_name = "Oulu"
                autonomous_system_organization = "<PLACEHOLDER>"
                log_line = ServiceLog(
                    timestamp=timestamp,
                    service=service,
                    requested_service=requested_service,
                    ip=ip,
                    longitude=longitude,
                    latitude=latitude,
                    autonomous_system_organization=autonomous_system_organization,
                    country_name=country_name,
                    city_name=city_name,
                    user=user,
                    event=event,
                    message="",
                    http_status=http_status,
                    user_agent=user_agent,
                    request_method=request_method,
                    content_size=content_size,
                    is_tor=False
                )
                log_line.save()
                # print(datetime.fromtimestamp(timestamp))
                if i % 100 == 0:
                    logger.info(f"Parsed {name} log until line {i}")

        if service.log_position < i:
            service.log_position = i
            service.save()

    logger.info(f"End logging for {name} job")


if __name__ == '__main__':
    run()
