from rest_framework import serializers
from .models import Position, Telemetry, TestData

# serializers translate the models into a different formats like JSON


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
        fields = ['pk', 'packet', 'random_int']
