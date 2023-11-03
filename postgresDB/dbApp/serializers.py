from rest_framework import serializers
from .models import Position, Telemetry, TestData, TerminalOutput

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

class TestDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestData
        fields = ['pk', 'rand_int']

class TerminalOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = TerminalOutput
        fields = ['received_packet_id', 'transmit_table_id', 'terminal_output']
