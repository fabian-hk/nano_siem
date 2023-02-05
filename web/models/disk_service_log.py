from django.db import models

from .disk_service import DiskService


class DiskServiceLog(models.Model):
    timestamp = models.DateTimeField(db_index=True, auto_now_add=True)
    service = models.ForeignKey(DiskService, on_delete=models.CASCADE, db_index=True)
    available = models.BooleanField()
    free_space = models.BigIntegerField(default=0)
    used_space = models.BigIntegerField(default=0)
