import logging
import time
from datetime import datetime, timedelta
from django.shortcuts import render
from django.utils.timezone import make_aware
from django.http import HttpResponse
import matplotlib.pyplot as plt
import io

from .models import OverwatchService, OverwatchLog
from plugins import overwatch

logger = logging.getLogger(__name__)


def overwatch_view(request):
    context = overwatch.get_data_as_table()
    return render(request, "overwatch_view.html", context)


def latency_plot(request, name):
    service = OverwatchService.objects.get(name=name)

    start_date = make_aware(datetime.today() - timedelta(days=7))
    logs = (
        OverwatchLog.objects.filter(service=service, timestamp__gte=start_date)
        .order_by("timestamp")
        .all()
    )

    timestamps = []
    latencies = []
    for log in logs:
        timestamps.append(log.timestamp)
        latencies.append(log.latency)

    plt.figure(figsize=(10, 5))
    plt.rcParams["font.size"] = 12
    plt.plot(timestamps, latencies)
    plt.title(name)
    plt.xlabel("Time")
    plt.ylabel("Latency (ms)")
    svg_str = io.BytesIO()
    plt.savefig(svg_str, format="svg")
    plt.close()

    return HttpResponse(svg_str.getvalue(), content_type="image/svg+xml")
