import logging
from datetime import datetime, timedelta
from django.shortcuts import render
from django.utils.timezone import make_aware
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import matplotlib.pyplot as plt
import io

from .models import NetworkService, NetworkServiceLog, DiskService, DiskServiceLog
from plugins import overwatch

logger = logging.getLogger(__name__)


@login_required
def overwatch_view(request):
    context = overwatch.get_data_as_table()
    return render(request, "overwatch_view.html", context)


def plot_network_service(name: str, type: str):
    service = NetworkService.objects.get(name=name, type=type)

    start_date = make_aware(datetime.today() - timedelta(days=7))
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

    start_date = make_aware(datetime.today() - timedelta(days=7))
    logs = (
        DiskServiceLog.objects.filter(service=service, timestamp__gte=start_date)
        .order_by("timestamp")
        .all()
    )

    timestamps = []
    availability = []
    for log in logs:
        timestamps.append(log.timestamp)
        availability.append(int(log.available))

    plt.plot(timestamps, availability)
    plt.title(f"{service.name} Availability Plot")
    plt.ylabel("Available")
    plt.ylim([0, 1.5])


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
