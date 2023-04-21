# Create your views here.
from .models import Position, Telemetry
from .serializers import PositionSerializer, TelemetrySerializer
from rest_framework import generics

# API endpoint that allows data to be viewed.


class PositionList(generics.RetrieveAPIView):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer


class TelemetryList(generics.RetrieveAPIView):
    queryset = Telemetry.objects.all()
    serializer_class = TelemetrySerializer

