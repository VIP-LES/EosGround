# Create your views here.
import json

from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from .forms import TerminalInputForm

from .models import Position, Telemetry, TestData, TerminalOutput, TransmitTable
from .serializers import PositionSerializer, TelemetrySerializer, TestDataSerializer, TerminalOutputSerializer
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from EosLib.device import Device
#from EosLib.format import Type
from EosLib.format.definitions import Type
from EosLib.format.formats.cutdown import CutDown
from EosLib.format.formats.ping_format import Ping
from EosLib.packet import Packet
from EosLib.packet.data_header import DataHeader
from EosLib.packet.definitions import Priority
import datetime

# API endpoint that allows data to be viewed.


class PositionList(generics.RetrieveAPIView):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer


class TelemetryList(generics.RetrieveAPIView):
    queryset = Telemetry.objects.all()
    serializer_class = TelemetrySerializer


class TestDataList(generics.RetrieveAPIView):
    queryset = TestData.objects.all()
    serializer_class = TestDataSerializer

class TerminalOutputList(generics.ListAPIView):
    queryset = TerminalOutput.objects.all()
    serializer_class = TerminalOutputSerializer


@api_view(['POST'])
def transmitTableInsert(request, ack: int=0):
    if request.method == 'POST':
        #input = request.POST.get('input')
        form = TerminalInputForm(request.POST)
        if form.is_valid():
            input = form.cleaned_data['command']
            if input.startswith('cut'):
                cutdown = CutDown(ack)
                cutdown_packet = Packet(cutdown, DataHeader(Device.GROUND_STATION_1, Type.CUTDOWN, Priority.TELEMETRY))
                cutdown_packet_binary = cutdown_packet.encode()
                transmitTable = TransmitTable()
                transmitTable.body = cutdown_packet_binary
                transmitTable.save()
                return Response({'message': 'Ping command received and processed'}, status=status.HTTP_200_OK)
            elif input.startswith('ping'):
                ping = Ping(True, ack)
                ping_packet = Packet(ping, DataHeader(Device.GROUND_STATION_1, Type.PING, Priority.TELEMETRY))
                ping_packet_binary = ping_packet.encode()
                transmitTable = TransmitTable()
                transmitTable.body = ping_packet_binary
                transmitTable.save()
                return Response({'message': 'Ping command received and processed'}, status=status.HTTP_200_OK)

            else:
                 return Response({'error': 'Invalid command'}, status=status.HTTP_400_BAD_REQUEST)

    return Response({'Hello': 'Invalid input or method'}, status=status.HTTP_400_BAD_REQUEST)










