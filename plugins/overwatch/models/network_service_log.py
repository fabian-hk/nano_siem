from django.db import models

from .network_service import NetworkService


class NetworkServiceLog(models.Model):
    timestamp = models.DateTimeField(db_index=True, auto_now_add=True)
    service = models.ForeignKey(NetworkService, on_delete=models.CASCADE, db_index=True)
    latency = models.FloatField()
