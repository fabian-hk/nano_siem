import logging
from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.timezone import make_aware
from folium import Map, Marker
from folium.plugins import FastMarkerCluster, MarkerCluster, HeatMap
import time
from datetime import datetime, timedelta

from .models import Service, ServiceLog

logger = logging.getLogger(__name__)

time_format_str = "%Y-%m-%d"


# Create your views here.
def overview_map_view(request):
    logger.info("Loading overview map...")
    start_coords = (48.78232, 9.17702)
    folium_map = Map(location=start_coords, zoom_start=4)

    t1 = time.time()
    loc_data = []
    timestamp_data = []
    for log_line in (
        ServiceLog.objects.filter(longitude__isnull=False, latitude__isnull=False)
        .order_by("-timestamp")
        .values("timestamp", "longitude", "latitude")[:2000000]
    ):
        loc_data.append([log_line["longitude"], log_line["latitude"]])
        timestamp_data.append(log_line["timestamp"])

    HeatMap(loc_data).add_to(folium_map)
    # FastMarkerCluster(loc_data).add_to(folium_map)
    logger.debug(f"Time to load {len(loc_data)} data points: {time.time() - t1}s")

    context = {
        "map": folium_map._repr_html_(),
        "start_date": timestamp_data[-1].strftime(time_format_str),
        "end_date": timestamp_data[0].strftime(time_format_str),
    }
    return render(request, "overview_map_view.html", context)


class MarkerPoint:
    def __init__(self, longitude=None, latitude=None):
        self.longitude = longitude
        self.latitude = latitude
        self.entries = 1

        self.ips = []
        self.http_statuses = []
        self.requested_services = []
        self.events = []
        self.user_agents = []
        self.city_names = []
        self.country_names = []

    def fill_data(self, log_line: ServiceLog):
        self.ips.append(log_line.ip)
        self.http_statuses.append(log_line.http_status)
        self.requested_services.append(log_line.requested_service)
        self.events.append(
            log_line.event.replace("{", "<BRACKETS>").replace("}", "<BRACKETS>")
        )
        self.user_agents.append(
            log_line.user_agent.replace("{", "<BRACKETS>").replace("}", "<BRACKETS>")
        )
        self.city_names.append(log_line.city_name)
        self.country_names.append(log_line.country_name)

    def pop_up(self):
        limit_show = 20
        variables = {
            "table_list": zip(
                self.ips[:limit_show],
                self.http_statuses[:limit_show],
                self.requested_services[:limit_show],
                self.events[:limit_show],
                self.user_agents[:limit_show],
                self.city_names[:limit_show],
                self.country_names[:limit_show],
            )
        }
        return render_to_string("detailed_map_view_table.html", variables)

    def __repr__(self):
        return f"({self.longitude}, {self.latitude})"

    def __eq__(self, other):
        if isinstance(other, MarkerPoint):
            return other.latitude == self.latitude and other.longitude == self.longitude
        else:
            return False

    def __hash__(self):
        return hash(self.__repr__())


def detailed_map_view(request):
    date_range = int(request.GET.get("date_range", "0"))
    if date_range == 0:
        start_date_default = datetime.today() - timedelta(days=7)
        start_date_str = request.GET.get(
            "start_date", start_date_default.strftime(time_format_str)
        )
        end_date_str = request.GET.get(
            "end_date", datetime.today().strftime(time_format_str)
        )
        start_date = make_aware(datetime.strptime(start_date_str, time_format_str))
        end_date = make_aware(datetime.strptime(end_date_str, time_format_str))
    else:
        start_date = datetime.today() - timedelta(days=date_range)
        start_date_str = start_date.strftime(time_format_str)
        start_date = make_aware(start_date)
        end_date = datetime.today()
        end_date_str = end_date.strftime(time_format_str)
        end_date = make_aware(end_date)

    logger.info(f"Loading detailed map from {start_date_str} to {end_date_str}")

    start_coords = (48.78232, 9.17702)
    folium_map = Map(location=start_coords, zoom_start=4)
    t1 = time.time()
    marker_cluster = MarkerCluster().add_to(folium_map)
    prev_marker_point = MarkerPoint()
    i = 0
    for i, log_line in enumerate(
        ServiceLog.objects.filter(
            timestamp__gte=start_date, timestamp__lte=end_date
        ).order_by("longitude", "latitude")
    ):
        if log_line.longitude and log_line.latitude:
            marker_point = MarkerPoint(log_line.longitude, log_line.latitude)
            if marker_point == prev_marker_point:
                prev_marker_point.fill_data(log_line)
                prev_marker_point.entries += 1
            else:
                if prev_marker_point != MarkerPoint():
                    Marker(
                        location=(
                            prev_marker_point.longitude,
                            prev_marker_point.latitude,
                        ),
                        popup=prev_marker_point.pop_up(),
                        tooltip=prev_marker_point.entries,
                    ).add_to(marker_cluster)

                marker_point.fill_data(log_line)
                prev_marker_point = marker_point
    if prev_marker_point != MarkerPoint():
        Marker(
            location=(prev_marker_point.longitude, prev_marker_point.latitude),
            popup=prev_marker_point.pop_up(),
            tooltip=prev_marker_point.entries,
        ).add_to(marker_cluster)

    logger.debug(f"Time to load {i} data points: {time.time() - t1}s")

    context = {
        "map": folium_map._repr_html_(),
        "start_date": start_date_str,
        "end_date": end_date_str,
    }
    return render(request, "detailed_map_view.html", context=context)
