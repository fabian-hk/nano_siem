from django.db import models


class Service(models.Model):
    name = models.TextField(unique=True)
    type = models.CharField(max_length=40, db_index=True)
    log_position = models.BigIntegerField()
    log_path = models.TextField()
    modification_time = models.DateTimeField(auto_now=True)
    running = models.BooleanField(default=False)
