from django.db import models

from .overwatch_service import OverwatchService


class OverwatchLog(models.Model):
    timestamp = models.DateTimeField(db_index=True, auto_now_add=True)
    service = models.ForeignKey(
        OverwatchService, on_delete=models.CASCADE, db_index=True
    )
    latency = models.FloatField()
