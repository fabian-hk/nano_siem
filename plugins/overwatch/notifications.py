from .models import NetworkService, DiskService
from .view import get_data_as_table


def get_notification_data() -> dict:
    if sent_notifications():
        return get_data_as_table()
    return {}


def sent_notifications() -> bool:
    notify = False
    for service in NetworkService.objects.all():
        if not service.available and not service.notified:
            notify = True
            service.notified = True
            service.save()

    for service in DiskService.objects.all():
        if not service.available and not service.notified:
            notify = True
            service.notified = True
            service.save()

    return notify
