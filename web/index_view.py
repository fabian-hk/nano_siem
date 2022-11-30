import logging
from django.shortcuts import render

logger = logging.getLogger(__name__)


def index_view(request):
    return render(request, "index.html")
