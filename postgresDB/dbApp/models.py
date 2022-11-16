from django.db import models

# Create your models here.

class RawData(models.Model):
    packet_type = models.TextField()
    priority = models.TextField()
    device = models.TextField()
    body = models.TextField()