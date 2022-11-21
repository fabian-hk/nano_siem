from django.db import models

from .service import Service


class ServiceLog(models.Model):
    timestamp = models.DateTimeField(db_index=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, db_index=True)
    requested_service = models.TextField()
    ip = models.GenericIPAddressField()
    longitude = models.FloatField()
    latitude = models.FloatField()
    autonomous_system_organization = models.TextField()
    country_name = models.TextField()
    city_name = models.TextField()
    user = models.TextField()
    event = models.TextField()
    message = models.TextField()
    http_status = models.IntegerField()
    user_agent = models.TextField()
    request_method = models.CharField(max_length=10)
    content_size = models.IntegerField()
    is_tor = models.BooleanField()
