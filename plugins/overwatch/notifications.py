import os
from datetime import datetime
from django.utils.timezone import make_aware

from .models import NetworkService, DiskService
from .view import get_data_as_table


def get_notification_data() -> dict:
    if sent_notifications():
        return get_data_as_table()
    return {}


def sent_notifications() -> bool:
    notify = False
    for service in NetworkService.objects.all():
        if service.unavailable_since and (
            (  # Send notification email, if service is unavailable for 3 minutes
                not service.notified
                and (
                    make_aware(datetime.now()) - service.unavailable_since
                ).total_seconds()
                > int(os.getenv("OW_TIMEOUT_FIRST_NOTIFICATION", "180"))
            )
            or (  # Resend notification email, if service is still unavailable after 1 hour
                service.notified
                and (
                    make_aware(datetime.now()) - service.unavailable_since
                ).total_seconds()
                > int(os.getenv("OW_TIMEOUT_REMINDER_NOTIFICATION", "3600")) # TODO fix bug with resending every time after 1 hour
            )
        ):
            notify = True
            service.notified = True
            service.save()
        elif (
                not service.unavailable_since and service.notified
        ):  # Send notification email if service becomes available again
            notify = True
            service.notified = False
            service.save()

    for service in DiskService.objects.all():
        if not service.available and not service.notified:
            notify = True
            service.notified = True
            service.save()

    return notify
