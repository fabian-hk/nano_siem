import logging
import os
import io
from datetime import datetime, timedelta

from django.forms import model_to_dict
from django.shortcuts import render
from django.utils.timezone import make_aware
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import matplotlib.pyplot as plt

from plugins.overwatch.models import (
    NetworkService,
    NetworkServiceLog,
    DiskService,
    DiskServiceLog,
)

logger = logging.getLogger(__name__)


@login_required
def overwatch_view(request):
    context = get_data_as_table()
    return render(request, "overwatch/overwatch_view.html", context)


def plot_network_service(name: str, type: str):
    service = NetworkService.objects.get(name=name, type=type)

    start_date = make_aware(datetime.today() - timedelta(days=float(os.getenv("OW_LATENCY_PLOT_DAYS", "1"))))
    logs = (
        NetworkServiceLog.objects.filter(service=service, timestamp__gte=start_date)
        .order_by("timestamp")
        .all()
    )

    timestamps = []
    latencies = []
    for log in logs:
        timestamps.append(log.timestamp)
        latencies.append(log.latency)

    plt.plot(timestamps, latencies)
    plt.title(f"{service.name} Latency Plot")
    plt.ylabel("Latency (ms)")


def plot_disk_service(name: str, type: str):
    service = DiskService.objects.get(name=name, type=type)

    start_date = make_aware(datetime.today() - timedelta(days=float(os.getenv("OW_DISK_PLOT_DAYS", "30"))))
    logs = (
        DiskServiceLog.objects.filter(service=service, timestamp__gte=start_date)
        .order_by("timestamp")
        .all()
    )

    timestamps = []
    availability = []
    for log in logs:
        timestamps.append(log.timestamp)
        availability.append(int(log.used_space) / 10**9)

    plt.plot(timestamps, availability)
    plt.title(f"{service.name} Used Space Plot")
    plt.ylabel("Used Space (GB)")


@login_required
def latency_plot(request, name: str, type: str):
    plt.figure(figsize=(10, 5))
    plt.rcParams["font.size"] = 12
    if type == "disk":
        plot_disk_service(name, type)
    else:
        plot_network_service(name, type)
    plt.xlabel("Date")

    svg_str = io.BytesIO()
    plt.savefig(svg_str, format="svg")
    plt.close()

    return HttpResponse(svg_str.getvalue(), content_type="image/svg+xml")


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
        model_as_dict["details"] = (
            f"{service.host} // {service.port}" if service.port != 0 else service.host
        )
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
