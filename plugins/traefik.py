from pathlib import Path

import os
import django
import shlex
from datetime import datetime

# Prepare Django framework to make database transaction
os.environ["DJANGO_SETTINGS_MODULE"] = "nano_siem.settings"
django.setup()

from web.models import Service, ServiceLog

log_file = Path("../nano_siem_data/access.log.backup.3")
name = "Traefik"


class Traefik:
    def setup(self):
        service = Service(name="Traefik", type="traefik", log_position=0, log_path=str(log_file.resolve()))
        service.save()

    def run(self):
        service = Service.objects.get(name=name)
        i = 0
        with log_file.open("rt") as f:
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
                    http_status = data[6]
                    content_size = data[7]
                    longitude = 65.01236
                    latitude = 25.46816
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
                if i == 2:
                    break

        if service.log_position < i:
            service.log_position = i
            service.save()


if __name__ == '__main__':
    Traefik().run()
