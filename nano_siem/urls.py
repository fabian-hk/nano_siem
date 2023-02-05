"""nano_siem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth.views import LoginView
from web.index_view import index_view
from web.map_views import overview_map_view, detailed_map_view
from web.event_view import event_view
from web.overwatch_view import overwatch_view, latency_plot

urlpatterns = [
    #    path('admin/', admin.site.urls),
    path("", index_view, name="index"),
    path("map/overview/", overview_map_view, name="overview_map"),
    path("map/detailed/", detailed_map_view, name="detailed_map"),
    path("events/", event_view, name="events"),
    path("overwatch/", overwatch_view, name="overwatch"),
    path("api/overwatch/latency-plot/<str:type>/<str:name>", latency_plot, name="latency_plot"),
    path("oidc/", include("mozilla_django_oidc.urls")),
    path("accounts/login", LoginView.as_view(), name="login"),
]

# To serve static files directly with gunicorn
urlpatterns += staticfiles_urlpatterns()
