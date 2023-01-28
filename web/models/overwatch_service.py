from django.db import models


class OverwatchService(models.Model):
    name = models.TextField(unique=True)
    type = models.CharField(max_length=10, db_index=True)
    available = models.BooleanField()
    modification_time = models.DateTimeField(auto_now=True)
