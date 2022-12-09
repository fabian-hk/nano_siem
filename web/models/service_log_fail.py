from django.db import models

from .service import Service


class ServiceLogFail(models.Model):
    ip = models.GenericIPAddressField(db_index=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, db_index=True)
    message = models.TextField()
    seen = models.BooleanField(db_index=True, default=False)
    timestamp_create = models.DateTimeField(auto_now_add=True)
