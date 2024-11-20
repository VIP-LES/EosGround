from django.db import models

# creates models of the tables in the database to store values from it
# can be done quickly by running 'python manage.py inspectdb' once the database is connected

class Position(models.Model):
    packet = models.ForeignKey('ReceivedPackets', models.DO_NOTHING)
    timestamp = models.DateTimeField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    altitude = models.FloatField(blank=True, null=True)
    speed = models.FloatField(blank=True, null=True)
    num_satellites = models.IntegerField(blank=True, null=True)
    flight_state = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'position'


class ReceivedData(models.Model):
    raw_bytes = models.BinaryField()
    rssi = models.IntegerField()
    processed = models.BooleanField()
    received_time = models.DateTimeField(blank=True, null=True)

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


class Telemetry(models.Model):
    packet = models.ForeignKey(ReceivedPackets, models.DO_NOTHING)
    timestamp = models.DateTimeField(blank=True, null=True)
    temperature = models.FloatField(blank=True, null=True)
    pressure = models.FloatField(blank=True, null=True)
    humidity = models.FloatField(blank=True, null=True)
    x_rotation = models.FloatField(blank=True, null=True)
    y_rotation = models.FloatField(blank=True, null=True)
    z_rotation = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'telemetry'


class Science(models.Model):

    models.FloatField(blank=True, null=True)
    models.IntegerField(blank=True, null=True)

    packet = models.ForeignKey(ReceivedPackets, models.DO_NOTHING)
    temperature_celsius = models.FloatField(blank=True, null=True)  # from SHTC3 temperature-humidity sensor
    relative_humidity_percent = models.FloatField(blank=True, null=True)  # from SHTC3 temperature-humidity sensor
    temperature_celsius_2 = models.FloatField(blank=True, null=True)  # from BMP388 temperature-pressure sensor
    pressure_hpa = models.FloatField(blank=True, null=True)  # from BMP388 temperature-pressure sensor
    altitude_meters = models.FloatField(blank=True, null=True)  # from BMP388 temperature-pressure sensor
    ambient_light_count = models.IntegerField(blank=True, null=True)  # from LTR390 uv-light sensor
    ambient_light_lux = models.FloatField(blank=True, null=True)  # from LTR390 uv-light sensor
    uv_count = models.IntegerField(blank=True, null=True)  # from LTR390 uv-light sensor
    uv_index = models.FloatField(blank=True, null=True)  # from LTR390 uv-light sensor
    infrared_count = models.IntegerField(blank=True, null=True)  # from TSL2591 ir-light sensor
    visible_count = models.IntegerField(blank=True, null=True)  # from TSL2591 ir-light sensor
    full_spectrum_count = models.IntegerField(blank=True, null=True)  # from TSL2591 ir-light sensor
    ir_visible_lux = models.FloatField(blank=True, null=True)  # from TSL2591 ir-light sensor
    pm10_standard_ug_m3 = models.IntegerField(blank=True, null=True)  # from PMSA003I particulate sensor
    pm25_standard_ug_m3 = models.IntegerField(blank=True, null=True)  # from PMSA003I particulate sensor
    pm100_standard_ug_m3 = models.IntegerField(blank=True, null=True)  # from PMSA003I particulate sensor
    pm10_environmental_ug_m3 = models.IntegerField(blank=True, null=True)  # from PMSA003I particulate sensor
    pm25_environmental_ug_m3 = models.IntegerField(blank=True, null=True)  # from PMSA003I particulate sensor
    pm100_environmental_ug_m3 = models.IntegerField(blank=True, null=True)  # from PMSA003I particulate sensor
    particulate_03um_per_01L = models.IntegerField(blank=True, null=True)  # from PMSA003I particulate sensor
    particulate_05um_per_01L = models.IntegerField(blank=True, null=True)  # from PMSA003I particulate sensor
    particulate_10um_per_01L = models.IntegerField(blank=True, null=True)  # from PMSA003I particulate sensor
    particulate_25um_per_01L = models.IntegerField(blank=True, null=True)  # from PMSA003I particulate sensor
    particulate_50um_per_01L = models.IntegerField(blank=True, null=True)  # from PMSA003I particulate sensor
    particulate_100um_per_01L = models.IntegerField(blank=True, null=True)  # from PMSA003I particulate sensor

    class Meta:
        managed = False
        db_table = 'science'

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
    body = models.BinaryField()

    class Meta:
        managed = False
        db_table = 'transmit_table'

class TerminalOutput(models.Model):
    received_packet = models.ForeignKey(ReceivedPackets, on_delete=models.DO_NOTHING)
    transmit_table = models.ForeignKey(TransmitTable, on_delete=models.DO_NOTHING)
    terminal_output = models.CharField(max_length=255)
    class Meta:
        managed = False
        db_table = 'terminal_output'


