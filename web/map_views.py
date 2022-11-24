import logging
from django.http import HttpResponse
from django.template.loader import render_to_string
from folium import Map, Marker
from folium.plugins import FastMarkerCluster, MarkerCluster
import time
import datetime

from .models import Service, ServiceLog

logger = logging.getLogger(__name__)


# Create your views here.
def overview_map_view(request):
    logger.info("Loading overview map...")
    start_coords = (65.01236, 25.46816)
    folium_map = Map(location=start_coords, zoom_start=14)
    tooltip = "Click me!"

    t1 = time.time()
    markers = [[l.longitude, l.latitude] for l in ServiceLog.objects.all()]
    FastMarkerCluster(markers).add_to(folium_map)
    logger.debug(f"Time to load log data: {time.time() - t1}s")
    # for log_line in ServiceLog.objects.all()[:100000]:
    #    Marker(
    #        location=(log_line.longitude, log_line.latitude),
    #        radius=5,
    #        fill_opacity=0.9,
    #        popup="<h1>More info coming soon...</h1>",
    #        tooltip=tooltip).add_to(marker_cluster)
    return HttpResponse(folium_map._repr_html_())


class MarkerPoint:
    def __init__(self, longitude=0.0, latitude=0.0):
        self.longitude = longitude
        self.latitude = latitude
        self.entries = 1
        self.ips = []
        self.longitudes = []
        self.latitudes = []
        self.events = []

    def pop_up(self):
        limit_show = 20
        variables = {"table_list": zip(self.ips[:limit_show], self.longitudes[:limit_show], self.latitudes[:limit_show], self.events[:limit_show])}
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
    logger.info("Loading detailed map...")
    start_coords = (48.78232, 9.17702)
    folium_map = Map(location=start_coords, zoom_start=4)
    t1 = time.time()
    date = datetime.date(2021, 7, 1)
    marker_cluster = MarkerCluster().add_to(folium_map)
    prev_marker_point = MarkerPoint()
    i = 0
    for i, log_line in enumerate(ServiceLog.objects.all().order_by("longitude", "latitude")):
        if log_line.longitude and log_line.latitude:
            marker_point = MarkerPoint(log_line.longitude, log_line.latitude)
            if marker_point == prev_marker_point:
                prev_marker_point.ips.append(log_line.ip)
                prev_marker_point.longitudes.append(log_line.longitude)
                prev_marker_point.latitudes.append(log_line.latitude)
                prev_marker_point.events.append(log_line.event)
                prev_marker_point.entries += 1
            else:
                if prev_marker_point != MarkerPoint():
                    Marker(
                        location=(prev_marker_point.longitude, prev_marker_point.latitude),
                        popup=prev_marker_point.pop_up(),
                        tooltip=prev_marker_point.entries).add_to(marker_cluster)

                marker_point.ips.append(log_line.ip)
                marker_point.longitudes.append(log_line.longitude)
                marker_point.latitudes.append(log_line.latitude)
                marker_point.events.append(log_line.event)

                prev_marker_point = marker_point

    if prev_marker_point != MarkerPoint():
        Marker(
            location=(prev_marker_point.longitude, prev_marker_point.latitude),
            popup=prev_marker_point.pop_up(),
            tooltip=prev_marker_point.entries).add_to(marker_cluster)

    logger.debug(f"Time to load {i} data points: {time.time() - t1}s")

    return HttpResponse(folium_map._repr_html_())
