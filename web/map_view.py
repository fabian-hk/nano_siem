import logging
from django.http import HttpResponse
from folium import Map, Marker
from folium.plugins import FastMarkerCluster

from .models import Service, ServiceLog

logger = logging.getLogger(__name__)


# Create your views here.
def map_view(request):
    logger.info("Loading map...")
    start_coords = (65.01236, 25.46816)
    folium_map = Map(location=start_coords, zoom_start=14)
    tooltip = "Click me!"
    markers = [[l.longitude, l.latitude] for l in ServiceLog.objects.all()]
    marker_cluster = FastMarkerCluster(markers).add_to(folium_map)
    #for log_line in ServiceLog.objects.all()[:100000]:
    #    Marker(
    #        location=(log_line.longitude, log_line.latitude),
    #        radius=5,
    #        fill_opacity=0.9,
    #        popup="<h1>More info coming soon...</h1>",
    #        tooltip=tooltip).add_to(marker_cluster)
    return HttpResponse(folium_map._repr_html_())
