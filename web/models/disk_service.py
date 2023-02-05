from django.db import models


class DiskService(models.Model):
    name = models.TextField()
    type = models.CharField(max_length=10, db_index=True)
    device = models.TextField()
    mount_point = models.TextField()
    uuid = models.TextField(null=True)
    available = models.BooleanField(default=True)
    notified = models.BooleanField(default=False)
    modification_time = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("name", "type")