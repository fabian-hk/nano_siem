from django.db import models
from datetime import datetime
from django.utils.timezone import make_aware


class BaseModel(models.Model):
    name = models.TextField()
    type = models.CharField(max_length=10, db_index=True)
    unavailable_since = models.DateTimeField(null=True, default=None)
    notified = models.BooleanField(default=False)
    modification_time = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        unique_together = ("name", "type")

    def available(self):
        self.unavailable_since = None
        self.save()

    def unavailable(self):
        if not self.unavailable_since:
            self.unavailable_since = make_aware(datetime.now())
        self.save()
