# Create your models here.

from django.db import models

class ReceivedData(models.Model):
    raw_bytes = models.BinaryField()
    rssi = models.IntegerField()
    processed = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'received_data'


class ReceivedPackets(models.Model):
    data = models.ForeignKey(ReceivedData, models.DO_NOTHING)
    packet_type = models.IntegerField()
    sender = models.IntegerField()
    priority = models.IntegerField()
    destination = models.IntegerField()
    generate_time = models.DateTimeField()
    sequence_number = models.IntegerField()
    send_time = models.DateTimeField()
    received_time = models.DateTimeField()
    packet_body = models.BinaryField()
    processed = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'received_packets'


class Temperature(models.Model):
    packet = models.ForeignKey(ReceivedPackets, models.DO_NOTHING)
    temperature = models.FloatField()

    class Meta:
        managed = False
        db_table = 'temperature'


class TestData(models.Model):
    packet = models.ForeignKey(ReceivedPackets, models.DO_NOTHING)
    random_int = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'test_data'


class TransmitTable(models.Model):
    time_sent = models.DateTimeField(blank=True, null=True)
    packet_type = models.IntegerField()
    sender = models.IntegerField()
    priority = models.IntegerField()
    destination = models.IntegerField()
    generate_time = models.DateTimeField()
    body = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'transmit_table'
