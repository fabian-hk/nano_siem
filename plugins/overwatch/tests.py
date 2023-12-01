from django.test import TestCase
from datetime import timedelta
from django.utils import timezone

from .models import NetworkService, DiskService
from .notifications import sent_notifications


class TestOverwatch(TestCase):
    network_service: NetworkService = None
    disk_service: DiskService = None

    def setUp(self):
        self.network_service = NetworkService.objects.create(
            name="test", type="http", unavailable_since=None, notified=False
        )
        self.network_service.save()

        self.disk_service = DiskService.objects.create(
            name="test", type="disk", unavailable_since=None, notified=False
        )
        self.disk_service.save()

    def test_notification_condition_good(self):
        # Do not notify on availability
        self.assertFalse(sent_notifications())

        # Notify after 3 minutes of unavailability
        self.network_service.refresh_from_db()
        self.network_service.unavailable_since = timezone.now() - timedelta(seconds=181)
        self.network_service.save()
        self.assertTrue(sent_notifications())

        # Do not notify between 3 and 1 hour
        self.network_service.refresh_from_db()
        self.network_service.unavailable_since = timezone.now() - timedelta(seconds=3500)
        self.network_service.save()
        self.assertFalse(sent_notifications())

        # Notify again after 1 hour
        self.network_service.refresh_from_db()
        self.network_service.unavailable_since = timezone.now() - timedelta(seconds=3601)
        self.network_service.save()
        self.assertFalse(sent_notifications())

    def test_notification_condition_wrong_db(self):
        """
        Test if notifications are sent, if the database is not in the correct state.
        """
        self.network_service.unavailable_since = timezone.now() - timedelta(seconds=7201)
        self.network_service.notified = False
        self.network_service.save()
        self.assertTrue(sent_notifications())

        self.assertFalse(sent_notifications())

        self.assertFalse(sent_notifications())

    def test_notification_network_and_disk(self):
        self.disk_service.unavailable_since = timezone.now() - timedelta(seconds=181)
        self.disk_service.save()

        self.assertTrue(sent_notifications())

        self.assertFalse(sent_notifications())

    def test_mixed_availability(self):
        self.assertFalse(sent_notifications())

        self.network_service.unavailable_since = timezone.now() - timedelta(seconds=140)
        self.network_service.save()
        self.assertFalse(sent_notifications())

        self.network_service.refresh_from_db()
        self.disk_service.unavailable_since = None
        self.disk_service.save()
        self.assertFalse(sent_notifications())

        self.network_service.refresh_from_db()
        self.network_service.unavailable_since = timezone.now() - timedelta(seconds=179)
        self.network_service.save()
        self.assertFalse(sent_notifications())

        self.network_service.refresh_from_db()
        self.network_service.unavailable_since = timezone.now() - timedelta(seconds=181)
        self.network_service.save()
        self.assertTrue(sent_notifications())

        self.network_service.refresh_from_db()
        self.network_service.unavailable_since = None
        self.network_service.save()
        self.assertTrue(sent_notifications())

        self.assertFalse(sent_notifications())

    def tearDown(self):
        pass
