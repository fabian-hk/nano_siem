import os
import logging
import shlex
from datetime import datetime

from plugins.http_logs.modules import parse_log_lines, get_service, ParsedLogLine
from plugins.http_logs.utils import str_to_int, IDS_SCORE_PARSER_FAILURE
from plugins.http_logs.models import Service

logger = logging.getLogger(__name__)


def parse_traefik_log_line(line: str, line_nr: int, service: Service) -> ParsedLogLine:
    """
    Method to parse a log line from a Traefik access log file.

    **If you want to parse log lines from a different service,
    you have to implement a method like this one.**

    :param line:        Log line in string format to be parsed
    :param line_nr:     Line number of the log line in the log file
    :param service:     Service the log line belongs to
    :return:            ParsedLogLine object that has to contain a timestamp and
                        should contain an IP address in any case
    """
    parsed_log_line = ParsedLogLine()
    try:
        # Strip new line character at the end
        # Replace "" with "'. This is necessary because some
        # user agent strings have "" at the beginning.
        # This is probably some kind of injection attack
        # to prevent log parsers from correctly parsing the
        # log line.
        line_preprocessed = (
            line.rstrip("\n").replace('"" ', "'\" ").replace(' ""', " \"'")
        )
        data = shlex.split(line_preprocessed)
        parsed_log_line.ip = data[0]
        raw_date = f"{data[3].lstrip('[')} {data[4].rstrip(']')}"
        parsed_log_line.timestamp = datetime.strptime(raw_date, "%d/%b/%Y:%H:%M:%S %z")
        parsed_log_line.requested_service = data[11]
        parsed_log_line.user = data[2]
        event_request_method = data[5].split(" ")
        parsed_log_line.event = event_request_method[1]
        parsed_log_line.request_method = event_request_method[0]
        parsed_log_line.user_agent = data[9]
        parsed_log_line.http_status = str_to_int(data[6])
        parsed_log_line.content_size = str_to_int(data[7])
    except Exception as e:
        print(e)
        logger.error(
            f"Could not parse log line {line_nr} for job {service.name}, line: {line}"
        )
        # Save failed log line to the ServiceLog table
        line_split = line.split(" ")
        parsed_log_line.ip = line_split[0]
        raw_date = f"{line_split[3].lstrip('[')} {line_split[4].rstrip(']')}"
        parsed_log_line.timestamp = datetime.strptime(raw_date, "%d/%b/%Y:%H:%M:%S %z")
        parsed_log_line.message = line
        parsed_log_line.ids_score = IDS_SCORE_PARSER_FAILURE

    return parsed_log_line


def get_traefik_service() -> Service:
    # Load configuration
    name = os.getenv("TRAEFIK_SERVICE_NAME", "Traefik")
    log_path = os.getenv("TRAEFIK_SERVICE_LOG_PATH", "/var/log/traefik_access.log")

    return get_service(name, "traefik", log_path)


def run():
    """
    Method to run the Traefik log parser.
    It has to be called from the plugins.http_logs.cronjob module.
    """
    service = get_traefik_service()
    parse_log_lines(service, parse_traefik_log_line)
