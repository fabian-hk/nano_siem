from pathlib import Path

import os
from datetime import datetime
import logging

from django.utils.timezone import make_aware

from plugins.http_logs.models import Service, ServiceLog
from plugins.http_logs.utils import ip_to_coordinates, IDSRules, CheckTor, IDS_SCORE_PARSER_FAILURE

logger = logging.getLogger(__name__)


class ParsedLogLine:
    timestamp: datetime  # Should be a timestamp with timezone information
    requested_service: str = None
    ip: str = None
    user: str = None
    event: str = None
    message: str = None
    http_status: int = None
    user_agent: str = None
    request_method: str = None
    content_size: int = 0
    ids_score: float = -1.0


def parse_log_lines(service: Service, parse_log_line):
    # Only run this job if the log file exists
    if not is_configured(service):
        return

    # Don't start the job if it is already running
    if service.running:
        logger.info(f"Log parsing job {service.name} already running")
        return

    logger.info(f"Start log parsing for {service.name} job")

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
                    parsed_log_line = parse_log_line(line, i, service)
                    log_line = ServiceLog(
                        timestamp=parsed_log_line.timestamp,
                        service=service,
                        requested_service=parsed_log_line.requested_service,
                        ip=parsed_log_line.ip,
                        user=parsed_log_line.user,
                        event=parsed_log_line.event,
                        message=parsed_log_line.message,
                        http_status=parsed_log_line.http_status,
                        user_agent=parsed_log_line.user_agent,
                        request_method=parsed_log_line.request_method,
                        content_size=parsed_log_line.content_size,
                        ids_score=parsed_log_line.ids_score,
                    )
                    ip_to_coordinates(parsed_log_line.ip, log_line)
                    log_line.is_tor = check_tor.is_tor_exit_node(parsed_log_line.ip)
                    if log_line.ids_score == -1.0:
                        log_line.ids_score = ids_rules.ids_score(
                            parsed_log_line.event, parsed_log_line.user_agent
                        )
                except Exception as e:
                    print(e)
                    logger.error(
                        f"Could not parse log line {i} for job {service.name}, line: {line}"
                    )
                    log_line = ServiceLog(
                        timestamp=make_aware(datetime.now()),
                        service=service,
                        message=line,
                        ids_score=IDS_SCORE_PARSER_FAILURE,
                    )

                transaction_bulk.append(log_line)

                if i % 1000 == 0:
                    # Optimizing database transaction by committing 1000 log lines at once
                    ServiceLog.objects.bulk_create(
                        transaction_bulk, ignore_conflicts=True
                    )
                    transaction_bulk.clear()

                    logger.debug(f"Parsed {service.name} log until line {i}")
                    service.log_position = i
                    service.save()

        if service.log_position < i:
            # Save remaining log lines to the database
            ServiceLog.objects.bulk_create(transaction_bulk, ignore_conflicts=True)
            transaction_bulk.clear()

            logger.info(f"Parsed log until line {i} for service {service.name}")
            service.log_position = i
            service.save()

    # ids_rules.print_ids_stats()

    logger.info(f"End log parsing for {service.name} job")
    service.running = False
    service.save()


def is_configured(service: Service) -> bool:
    log_file = Path(service.log_path)
    return log_file.exists() and os.stat(service.log_path).st_size > 0


def get_service(name: str, type: str, log_path: str) -> Service:
    if Service.objects.filter(name=name).exists():
        # If service already exists update its attributes
        service = Service.objects.get(name=name)
        service.name = name
        service.log_path = log_path
        service.save()
    else:
        # If the service doesn't exist create it
        service = Service(
            name=name, type=type, log_position=-1, log_path=log_path, running=False
        )
        service.save()
        logger.info(f"Created new {type} job {name}")
    return service
