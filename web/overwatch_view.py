import logging
import time
from datetime import datetime, timedelta
from django.shortcuts import render
from django.utils.timezone import make_aware
from django.forms.models import model_to_dict

from .models import OverwatchService, OverwatchLog

logger = logging.getLogger(__name__)


def overwatch_view(request):
    rows = []
    for service in OverwatchService.objects.order_by("type").all():
        up = OverwatchLog.objects.filter(service=service).exclude(latency__exact=0.0).count()
        number = OverwatchLog.objects.filter(service=service).count()
        up_time = up / number
        model_as_dict = model_to_dict(service)
        model_as_dict["up_time"] = f"{int(up_time * 100)}%"
        model_as_dict["modification_time"] = service.modification_time
        rows.append(model_as_dict)

    context = {
        "services_header": ["Name", "Type", "Available", "Up-Time", "Last Updated"],
        "services": rows,
    }
    return render(request, "overwatch_view.html", context)
