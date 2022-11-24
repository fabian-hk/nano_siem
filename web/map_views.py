import logging
from django.http import HttpResponse
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
        html = """
            <table style="display: block; height: 100px; overflow: auto;">
            <thead>
                <tr>
                    <td style="background: white; position: sticky; top: 0;">IP</td>
                    <td style="background: white; position: sticky; top: 0; padding-left: 10px;">Longitude</td>
                    <td style="background: white; position: sticky; top: 0; padding-left: 10px;">Latitude</td>
                    <td style="background: white; position: sticky; top: 0; padding-left: 10px;">Event</td>
                </tr>
            </thead>
            <tbody>
        """
        limit_show = 20
        for (ip, longitude, latitude, event) in zip(self.ips[:limit_show], self.longitudes[:limit_show], self.latitudes[:limit_show], self.events[:limit_show]):
            row = f"""
                <tr>
                    <td>{ip}</td>
                    <td style="padding-left: 10px;">{'{:.4f}'.format(longitude)}</td>
                    <td style="padding-left: 10px;">{'{:.4f}'.format(latitude)}</td>
                    <td style="padding-left: 10px;">{event}</td>
                </tr>
            """
            html += row
        end = """
            </tbody>
        </table>  
        """
        html += end
        return html

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
    start_coords = (65.01236, 25.46816)
    folium_map = Map(location=start_coords, zoom_start=14)
    tooltip = "Click me!"
    t1 = time.time()
    date = datetime.date(2021, 7, 1)
    marker_points = []
    prev_marker_point = MarkerPoint()
    for log_line in ServiceLog.objects.all().order_by("longitude", "latitude"):
        marker_point = MarkerPoint(log_line.longitude, log_line.latitude)
        if marker_point == prev_marker_point:
            prev_marker_point.ips.append(log_line.ip)
            prev_marker_point.longitudes.append(log_line.longitude)
            prev_marker_point.latitudes.append(log_line.latitude)
            prev_marker_point.events.append(log_line.event)
            prev_marker_point.entries += 1
        else:
            marker_point.ips.append(log_line.ip)
            marker_point.longitudes.append(log_line.longitude)
            marker_point.latitudes.append(log_line.latitude)
            marker_point.events.append(log_line.event)
            marker_points.append(marker_point)
            prev_marker_point = marker_point
    logger.debug(f"Time to load {len(marker_points)} data points: {time.time() - t1}s")

    t1 = time.time()
    marker_cluster = MarkerCluster().add_to(folium_map)
    for marker_point in marker_points:
        Marker(
            location=(marker_point.longitude, marker_point.latitude),
            popup=marker_point.pop_up(),
            tooltip=marker_point.entries).add_to(marker_cluster)
    logger.debug(f"Time to create markers: {time.time() - t1}s")
    return HttpResponse(folium_map._repr_html_())
