from typing import List
import logging
import os
import io
from datetime import datetime, timedelta

from django.forms import model_to_dict
from django.shortcuts import render
from django.utils.timezone import make_aware
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objs as go

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


def smooth_plots(timestamps: List[datetime], values: List[float], kernel_size: int):
    if len(values) > 2 * kernel_size:
        values = np.convolve(values, np.ones(kernel_size) / kernel_size, mode="valid")
        timestamps = timestamps[kernel_size // 2 : -kernel_size // 2 + 1]
    return timestamps, values


def plot_network_service(name: str, type: str) -> go.Figure:
    service = NetworkService.objects.get(name=name, type=type)

    start_date = make_aware(
        datetime.today() - timedelta(days=float(os.getenv("OW_LATENCY_PLOT_DAYS", "1")))
    )
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

    kernel_size = int(os.getenv("OW_LATENCY_PLOT_SMOOTHING", "60"))
    timestamps, latencies = smooth_plots(timestamps, latencies, kernel_size)

    #plt.plot(timestamps, latencies)
    #plt.title(f"{service.name} Latency Plot")
    #plt.ylabel("Latency (ms)")
    fig = px.line(x=timestamps, y=latencies, title=f"{service.name} Latency Plot", labels={"x": "Date", "y": "Latency (ms)"})
    return fig



def plot_disk_service(name: str, type: str):
    service = DiskService.objects.get(name=name, type=type)

    start_date = make_aware(
        datetime.today() - timedelta(days=float(os.getenv("OW_DISK_PLOT_DAYS", "30")))
    )
    logs = (
        DiskServiceLog.objects.filter(service=service, timestamp__gte=start_date)
        .order_by("timestamp")
        .all()
    )

    timestamps = []
    availability = []
    for log in logs:
        timestamps.append(log.timestamp)
        availability.append(int(log.used_space) / 10 ** 9)

    kernel_size = int(os.getenv("OW_DISK_PLOT_SMOOTHING", "60"))
    timestamps, availability = smooth_plots(timestamps, availability, kernel_size)

    plt.plot(timestamps, availability)
    plt.title(f"{service.name} Used Space Plot")
    plt.ylabel("Used Space (GB)")


@login_required
def latency_plot(request):
    type = request.GET.get("type", default=None)
    name = request.GET.get("name", default=None)

    if type is None or name is None:
        return HttpResponse(status=400)

    
    if type == "disk":
        plt.figure(figsize=(10, 5))
        plt.rcParams["font.size"] = 12
        plot_disk_service(name, type)
        plt.xlabel("Date")

        svg_str = io.BytesIO()
        plt.savefig(svg_str, format="svg")
        plt.close()

        return HttpResponse(svg_str.getvalue(), content_type="image/svg+xml")
    else:
        fig = plot_network_service(name, type)
        return HttpResponse(fig.to_html(full_html=False), content_type="text/html")
    


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
        model_as_dict["up_time"] = f"{up_time * 100:.2f}%"
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
        model_as_dict["up_time"] = f"{up_time * 100:.2f}%"
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
