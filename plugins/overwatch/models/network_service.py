from django.db import models

from .base_model import BaseModel


class NetworkService(BaseModel):
    host = models.TextField(default="")
    port = models.IntegerField(default=0)
