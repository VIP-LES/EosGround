from rest_framework import serializers
from .models import Position, Telemetry, Science, TestData, TerminalOutput

# serializers translate the models into a different formats like JSON
# pk stands for primary key and Django automatically creates this for you

class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ['pk', 'packet', 'timestamp', 'latitude', 'longitude',
                  'altitude', 'speed', 'num_satellites', 'flight_state']


class TelemetrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Telemetry
        fields = ['pk', 'packet', 'timestamp', 'temperature', 'pressure',
                  'humidity', 'x_rotation', 'y_rotation', 'z_rotation']
        
class ScienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Science
        fields = ['pk', 'temperature_celsius', 'relative_humidity_percent',
                  'temperature_celsius_2', 'pressure_hpa', 'altitude_meters',
                  'ambient_light_count', 'ambient_light_lux', 'uv_count', 'uv_index',
                  'infrared_count', 'visible_count', 'full_spectrum_count', 'ir_visible_lux',
                  'pm10_standard_ug_m3', 'pm25_standard_ug_m3', 'pm100_standard_ug_m3',
                  'pm10_environmental_ug_m3', 'pm25_environmental_ug_m3', 'pm100_environmental_ug_m3',
                  'particulate_03um_per_01L', 'particulate_05um_per_01L', 'particulate_10um_per_01L',
                  'particulate_25um_per_01L', 'particulate_50um_per_01L', 'particulate_100um_per_01L']

class TestDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestData
        fields = ['pk', 'rand_int']

class TerminalOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = TerminalOutput
        fields = ['pk', 'received_packet_id', 'transmit_table_id', 'terminal_output']
