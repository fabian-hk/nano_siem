import os
from django.utils import timezone

from .models import NetworkService, DiskService
from .models.base_model import BaseModel
from .view import get_data_as_table


def get_notification_data() -> dict:
    if sent_notifications():
        return get_data_as_table()
    return {}


def sent_notifications() -> bool:
    notify = False
    notify |= check_services(NetworkService.objects.all())
    notify |= check_services(DiskService.objects.all())
    return notify


def check_services(services) -> bool:
    notify = False
    for service in services:
        # Send notification email if service becomes unavailable
        if notification_on_unavailability(service):
            notify = True
            service.notified = True
            service.save()
        # Send notification email if service becomes available again
        elif not service.unavailable_since and service.notified:
            notify = True
            service.notified = False
            service.save()
        # Notify once an hour if a service is unavailable
        elif service.notified and timezone.now().minute == 0:
            notify = True
    return notify


def notification_on_unavailability(service: BaseModel) -> bool:
    if not service.unavailable_since:
        return False

    t = (timezone.now() - service.unavailable_since).total_seconds()

    # Send notification email, if service is unavailable for a certain amount of time (default 3 minutes)
    return not service.notified and t > int(
        os.getenv("OW_TIMEOUT_FIRST_NOTIFICATION", "180")
    )
