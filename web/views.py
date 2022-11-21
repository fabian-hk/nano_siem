from django.http import HttpResponse
from folium import Map, Marker

from .models import Service, ServiceLog


# Create your views here.
def map_view(request):
    start_coords = (65.01236, 25.46816)
    folium_map = Map(location=start_coords, zoom_start=14)
    tooltip = "Click me!"
    for log_line in ServiceLog.objects.all():
        Marker([log_line.longitude, log_line.latitude], popup="<h1>More info coming soon...</h1>",
               tooltip=tooltip).add_to(folium_map)
    return HttpResponse(folium_map._repr_html_())
