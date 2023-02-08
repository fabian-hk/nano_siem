import logging
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from plugins.http_logs.models import Service, ServiceLog
from plugins.http_logs.utils.get_service import get_service

logger = logging.getLogger(__name__)


@login_required
def table_view(request):
    logger.info("Loading table view...")
    service = get_service()

    if request.method == "POST" and bool(request.POST.get("reset")):
        logger.warning(f"Log parsing job {service.name} was reset by user")
        service.running = False
        service.save()

    header = [
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

    max_events = 1000
    content = ServiceLog.objects.order_by("-timestamp").values(
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

    num_log_lines = ServiceLog.objects.all().count()
    cron_job_running = bool(service.running)

    context = {
        "header": header,
        "content": content,
        "num_log_lines": num_log_lines,
        "cron_job_running": cron_job_running,
    }
    return render(request, "http_logs/table_view.html", context)
