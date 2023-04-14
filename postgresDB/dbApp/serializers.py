from rest_framework import serializers
from .models import Position, Telemetry


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

