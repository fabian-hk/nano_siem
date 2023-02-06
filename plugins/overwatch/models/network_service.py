from django.db import models


class NetworkService(models.Model):
    name = models.TextField()
    type = models.CharField(max_length=10, db_index=True)
    host = models.TextField(default="")
    port = models.IntegerField(default=0)
    available = models.BooleanField(default=True)
    notified = models.BooleanField(default=False)
    modification_time = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("name", "type")
