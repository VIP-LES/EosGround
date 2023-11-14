# Create your views here.
import json
import os
import sys

from EosLib.format.formats.valve import Valve
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view


from .models import Position, Telemetry, TestData, TerminalOutput, TransmitTable
from .serializers import PositionSerializer, TelemetrySerializer, TestDataSerializer, TerminalOutputSerializer
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response

from EosLib.format.definitions import Type
from EosLib.format.formats.cutdown import CutDown
from EosLib.format.formats.ping_format import Ping
from EosLib.device import Device
from EosLib.packet import Packet
from EosLib.packet.data_header import DataHeader
from EosLib.packet.definitions import Priority
from datetime import datetime

# API endpoint that allows data to be viewed.

from django.db import connection
cursor = connection.cursor()

class PositionList(generics.RetrieveAPIView):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer


class TelemetryList(generics.RetrieveAPIView):
    queryset = Telemetry.objects.all()
    serializer_class = TelemetrySerializer


class TestDataList(generics.RetrieveAPIView):
    queryset = TestData.objects.all()
    serializer_class = TestDataSerializer


class TerminalOutputList(generics.RetrieveAPIView):
    queryset = TerminalOutput.objects.all()
    serializer_class = TerminalOutputSerializer


@api_view(['POST'])
def transmitTableInsert(request):
    try:
        if request.method == 'POST':
            terminal_input = json.loads(request.body)
            command = terminal_input["input"]
            ack = terminal_input["ack"]
            transmitTable = TransmitTable()
            transmitTable.sender = Device.GROUND_STATION_1
            transmitTable.priority = Priority.DATA
            transmitTable.generate_time = datetime.now()

            if command == "cutdown":
                cutdown_body = CutDown(ack)
                cutdown_body_bytes = cutdown_body.encode()
                transmitTable.packet_type = Type.CUTDOWN
                transmitTable.destination = Device.CUTDOWN
                transmitTable.body = cutdown_body_bytes
                transmitTable.save()
                cursor.execute("NOTIFY update;")
                connection.commit()
                return Response({'message': 'Cutdown command sent ', 'ack': ack}, status=status.HTTP_200_OK)
            elif command == "ping":
                ping_body = Ping(True, ack)
                ping_packet_bytes = ping_body.encode()
                transmitTable.packet_type = Type.PING
                transmitTable.destination = Device.MISC_RADIO_1
                transmitTable.body = ping_packet_bytes
                transmitTable.save()
                cursor.execute("NOTIFY update;")
                connection.commit()
                return Response({'message': 'Ping command sent ', 'ack': ack}, status=status.HTTP_200_OK)
            elif command == "valve":
                valve_body = Valve(ack)
                valve_body_bytes = valve_body.encode()
                transmitTable.packet_type = Type.VALVE
                transmitTable.destination = Device.VALVE
                transmitTable.body = valve_body_bytes
                transmitTable.save()
                cursor.execute("NOTIFY update;")
                connection.commit()
                return Response({'message': 'Valve command sent ', 'ack': ack}, status=status.HTTP_200_OK)

            return Response({'message': 'Invalid input or method'}, status=status.HTTP_400_BAD_REQUEST)

    except KeyError as e:
        # Handle the case where the expected keys are not present in the JSON data
        return Response({'message': f'Missing key: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
    except ValueError as e:
        # Handle the case where there's an issue with JSON decoding
        return Response({'message': f'Invalid JSON format: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        # Handle other unexpected errors
        return Response({'message': f'An error occurred: missing ack '}, status=status.HTTP_400_BAD_REQUEST)
