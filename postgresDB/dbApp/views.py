# Create your views here.
from .models import Position, Telemetry
from .serializers import PositionSerializer, TelemetrySerializer
from rest_framework import generics


class PositionList(generics.RetrieveAPIView):
    # API endpoint that allows data to be viewed.
    queryset = Position.objects.all()
    serializer_class = PositionSerializer


class TelemetryList(generics.RetrieveAPIView):
    # API endpoint that allows data to be viewed.
    queryset = Telemetry.objects.all()
    serializer_class = TelemetrySerializer

