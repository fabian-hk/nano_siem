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
from main.view import index_view
from main.user_authentication import login_proxy
from plugins.http_logs.map_views import overview_map_view, detailed_map_view
from plugins.http_logs.event_view import event_view
from plugins.http_logs.table_view import table_view
from plugins.overwatch.view import overwatch_view, latency_plot

urlpatterns = [
    #    path('admin/', admin.site.urls),
    path("", index_view, name="index"),
    path("logs/map/overview/", overview_map_view, name="overview_map"),
    path("logs/map/detailed/", detailed_map_view, name="detailed_map"),
    path("logs/events/", event_view, name="events"),
    path("logs/table/", table_view, name="log_table"),
    path("overwatch/", overwatch_view, name="overwatch"),
    path("api/overwatch/latency-plot/", latency_plot, name="latency_plot"),
    path("auth/login/", login_proxy, name="login_proxy"),
    path("oidc/", include("mozilla_django_oidc.urls")),
    path("accounts/login", LoginView.as_view(), name="login"),
]
