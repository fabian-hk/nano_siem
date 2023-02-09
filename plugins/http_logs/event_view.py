import logging
import time
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from plugins.http_logs.models import ServiceLog
from plugins.http_logs.utils import IDS_SCORE_PARSER_FAILURE

logger = logging.getLogger(__name__)


@login_required
def event_view(request):
    logger.info("Loading event view...")
    t = time.time()
    max_events = 30
    header_malicious = [
        "Timestamp",
        "Requested Service",
        "IP",
        "ASO",
        "Country Name",
        "City Name",
        "Event",
        "HTTP Status",
        "User Agent",
        "Request Method",
        "Is Tor",
        "IDS Score",
    ]
    malicious_events = (
        ServiceLog.objects.filter(longitude__isnull=False, latitude__isnull=False)
        .exclude(ids_score__exact=IDS_SCORE_PARSER_FAILURE)
        .order_by("-ids_score", "-timestamp")
        .values(
            "timestamp",
            "requested_service",
            "ip",
            "autonomous_system_organization",
            "country_name",
            "city_name",
            "event",
            "http_status",
            "user_agent",
            "request_method",
            "is_tor",
            "ids_score",
        )[:max_events]
    )
    logger.debug(f"Time to load malicious events: {time.time() - t}s")

    t = time.time()
    header_log_line_fail = [
        "Timestamp",
        "IP",
        "ASO",
        "Country Name",
        "City Name",
        "Message",
        "Is Tor",
        "IDS Score",
    ]
    log_line_fail_events = (
        ServiceLog.objects.filter(ids_score__exact=IDS_SCORE_PARSER_FAILURE)
        .order_by("-timestamp")
        .values(
            "timestamp",
            "ip",
            "autonomous_system_organization",
            "country_name",
            "city_name",
            "message",
            "is_tor",
            "ids_score",
        )[:max_events]
    )
    logger.debug(f"Time to load log line parse fail events: {time.time() - t}s")

    t = time.time()
    header_locationless = [
        "Timestamp",
        "Requested Service",
        "IP",
        "Event",
        "HTTP Status",
        "User Agent",
        "Request Method",
        "Is Tor",
        "IDS Score",
    ]
    locationless_events = (
        ServiceLog.objects.filter(longitude__isnull=True, latitude__isnull=True)
        .order_by("-timestamp")
        .values(
            "timestamp",
            "requested_service",
            "ip",
            "event",
            "http_status",
            "user_agent",
            "request_method",
            "is_tor",
            "ids_score",
        )[:max_events]
    )
    logger.debug(f"Time to load locationless log lines: {time.time() - t}s")

    t = time.time()
    tor_events = (
        ServiceLog.objects.filter(is_tor=True)
        .order_by("-ids_score", "-timestamp")
        .values(
            "timestamp",
            "requested_service",
            "ip",
            "autonomous_system_organization",
            "country_name",
            "city_name",
            "event",
            "http_status",
            "user_agent",
            "request_method",
            "is_tor",
            "ids_score",
        )[:max_events]
    )
    logger.debug(f"Time to load Tor log lines: {time.time() - t}s")

    context = {
        "header_malicious": header_malicious,
        "malicious_events": malicious_events,
        "header_log_line_fail": header_log_line_fail,
        "log_line_fail_events": log_line_fail_events,
        "header_locationless": header_locationless,
        "locationless_events": locationless_events,
        "header_tor": header_malicious,
        "tor_events": tor_events,
    }

    return render(request, "http_logs/event_view.html", context)
