from django.db import models
from django.utils import timezone
from django.contrib.postgres.fields import JSONField

# Create your models here.
class Traffic(models.Model):
    human_identifier = models.CharField(max_length=100)
    created_date = models.DateTimeField(default=timezone.now)
    flagged = models.BooleanField(default=False)
    metadata = JSONField()

    def __str__(self):
        return self.human_identifier
