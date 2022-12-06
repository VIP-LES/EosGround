from django.db import models

# Create your models here.

class RawData(models.Model):
    time_sent = models.DateTimeField(default="", blank=True)
    packet_type = models.IntegerField(default=1)
    packet_sender = models.IntegerField(default=1)
    packet_priority = models.IntegerField(default=1)
    packet_body = models.CharField(max_length=255, default="")

