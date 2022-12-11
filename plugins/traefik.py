from pathlib import Path

import os
import shlex
from datetime import datetime
import logging

from django.utils.timezone import make_aware

from web.models import Service, ServiceLog
from plugins.utils import str_to_int, ip_to_coordinates, IDSRules, CheckTor

logger = logging.getLogger(__name__)


def run(name, log_path):
    if Service.objects.filter(name=name).exists():
        # If service already exists update its attributes
        service = Service.objects.get(name=name)
        service.name = name
        service.log_path = log_path
        service.save()
    else:
        # If the service doesn't exist create it
        service = Service(
            name=name, type="traefik", log_position=-1, log_path=log_path, running=False
        )
        service.save()
        logger.info(f"Created new traefik job {name}")
    if not service.running:
        logger.info(f"Start log parsing for {name} job")
        # Mark service as running
        service.running = True
        service.save()

        # Prepare utils class
        ids_rules = IDSRules()
        check_tor = CheckTor()

        # Open log file
        log_file = Path(service.log_path)
        with log_file.open("rt") as f:
            i = 0
            transaction_bulk = []
            for i, line in enumerate(f):
                if i > service.log_position:
                    try:
                        # Strip new line character at the end
                        # Replace "" with "'. This is necessary because some
                        # user agent strings have "" at the beginning.
                        # This is probably some kind of injection attack
                        # to prevent log parsers from correctly parsing the
                        # log line.
                        line_preprocessed = (
                            line.rstrip("\n")
                            .replace('"" ', "'\" ")
                            .replace(' ""', " \"'")
                        )
                        data = shlex.split(line_preprocessed)
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
                        (
                            longitude,
                            latitude,
                            city_name,
                            country_name,
                            autonomous_system_organization,
                        ) = ip_to_coordinates(ip)
                        is_tor = check_tor.is_tor_exit_node(ip)
                        ids_score = ids_rules.ids_score(event, user_agent)

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
                            http_status=http_status,
                            user_agent=user_agent,
                            request_method=request_method,
                            content_size=content_size,
                            is_tor=is_tor,
                            ids_score=ids_score,
                        )
                        transaction_bulk.append(log_line)
                    except Exception as e:
                        print(e)
                        logger.error(
                            f"Could not parse log line {i} for job {name}, line: {line}"
                        )
                        # Save failed log line to the ServiceLog table
                        line_split = line.split(" ")
                        ip = line_split[0]

                        # Add as much information to the failed log as possible
                        (
                            longitude,
                            latitude,
                            city_name,
                            country_name,
                            autonomous_system_organization,
                        ) = ip_to_coordinates(ip)
                        is_tor = ids_rules.is_tor_exit_node(ip)

                        failed_log_line = ServiceLog(
                            timestamp=make_aware(datetime.now()),
                            ip=ip,
                            longitude=longitude,
                            latitude=latitude,
                            autonomous_system_organization=autonomous_system_organization,
                            country_name=country_name,
                            city_name=city_name,
                            is_tor=is_tor,
                            service=service,
                            message=line,
                            ids_score=999,
                            # set IDS score to a high value because it is most likely some kind of injection attack
                        )
                        transaction_bulk.append(failed_log_line)

                    if i % 1000 == 0:
                        # Optimizing database transaction by committing 1000 log lines at once
                        ServiceLog.objects.bulk_create(
                            transaction_bulk, ignore_conflicts=True
                        )
                        transaction_bulk.clear()

                        logger.debug(f"Parsed {name} log until line {i}")
                        service.log_position = i
                        service.save()

                if i == 1000000:
                    break

            if service.log_position < i:
                # Save remaining log lines to the database
                ServiceLog.objects.bulk_create(transaction_bulk, ignore_conflicts=True)
                transaction_bulk.clear()

                logger.info(f"Parsed log until line {i} for service {name}")
                service.log_position = i
                service.save()

        ids_rules.print_ids_stats()

        logger.info(f"End log parsing for {name} job")
        service.running = False
        service.save()
    else:
        logger.info(f"Log parsing job {name} already running")


if __name__ == "__main__":
    import django

    # Prepare Django framework to make database transaction
    os.environ["DJANGO_SETTINGS_MODULE"] = "nano_siem.settings"
    django.setup()
    logger.setLevel(logging.DEBUG)

    traefik_service_name = os.getenv("TRAEFIK_SERVICE_NAME")
    traefik_service_log_path = os.getenv("TRAEFIK_SERVICE_LOG_PATH")

    run(traefik_service_name, traefik_service_log_path)
