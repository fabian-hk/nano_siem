from django.db import models

from .base_model import BaseModel


class DiskService(BaseModel):
    device = models.TextField()
    mount_point = models.TextField()
    uuid = models.TextField(null=True)
