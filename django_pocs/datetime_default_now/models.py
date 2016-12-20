from django.db import models
from django.utils import timezone

from datetime import datetime

def get_timezone_aware_datetime_now():
    return timezone.make_aware(datetime.now())

class Post(models.Model):
    
    datetime = models.DateTimeField()

class PostWithDefaultDateTime(models.Model):

    datetime = models.DateTimeField(default=get_timezone_aware_datetime_now)
