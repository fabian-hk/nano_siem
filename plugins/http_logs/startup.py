import logging

import os
import django

# Prepare Django framework to make database transaction
os.environ["DJANGO_SETTINGS_MODULE"] = "nano_siem.settings"
django.setup()

from plugins.http_logs.models import Service

logger = logging.getLogger(__name__)


def reset_service_running_status():
    for service in Service.objects.all():
        service.running = False
        service.save()
        logger.info(f"Reset running status for {service.name} service")


if __name__ == "__main__":
    logger.setLevel(logging.INFO)
    reset_service_running_status()
