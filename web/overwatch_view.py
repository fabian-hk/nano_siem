import logging
import time
from django.shortcuts import render

from .models import OverwatchService, OverwatchLog

logger = logging.getLogger(__name__)


def overwatch_view(request):
    context = {
        "services_header": ["Name", "Type", "Available", "Last Updated"],
        "services": OverwatchService.objects.order_by("type"),
    }
    return render(request, "overwatch_view.html", context)
