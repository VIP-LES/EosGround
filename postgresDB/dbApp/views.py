# Create your views here.
from .models import Position, Telemetry, TestData
from .serializers import PositionSerializer, TelemetrySerializer, TestDataSerializer
from rest_framework import generics

# API endpoint that allows data to be viewed.


class PositionList(generics.RetrieveAPIView):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer
    
class AllPositions(generics.ListAPIView):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer


class TelemetryList(generics.RetrieveAPIView):
    queryset = Telemetry.objects.all()
    serializer_class = TelemetrySerializer


class TestDataList(generics.RetrieveAPIView):
    queryset = TestData.objects.all()
    serializer_class = TestDataSerializer
