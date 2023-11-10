# Create your views here.
import json
import os
import sys

from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from .forms import TerminalInputForm

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


# current_dir = os.path.dirname(os.path.abspath(__file__))
# parent_dir = os.path.dirname(current_dir)
# sys.path.append(parent_dir)
# grandparent_dir = os.path.dirname(parent_dir)
# sys.path.append(grandparent_dir)

# from EosGround.config.config import get_config
# import psycopg2

# API endpoint that allows data to be viewed.

# conn_params = get_config(os.path.normpath('database.ini'))
# #conn_params = get_config(os.path.join('./', 'database.ini'))
# #conn_params = get_config(os.path.join('EosGround', 'config', 'database.ini'))  # gets config params
# #conn_params = get_config(EosGr)
# conn = psycopg2.connect(**conn_params)  # gets connection object
# conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)  # sets up auto commit
# cursor = conn.cursor()  # creates cursor

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
    if request.method == 'POST':
        terminal_input = json.loads(request.body)
        command = terminal_input["input"]
        ack = terminal_input["ack"]
        transmitTable = TransmitTable()
        transmitTable.sender = Device.GROUND_STATION_1
        transmitTable.priority = Priority.DATA
        transmitTable.generate_time = datetime.now()

        # packet_sender = Device.GROUND_STATION_1
        # packet_priority = Priority.DATA
        # packet_generate_time = datetime.now()

        if command == "cutdown":
            cutdown_body = CutDown(ack)
            cutdown_body_bytes = cutdown_body.encode()
            transmitTable.packet_type = Type.CUTDOWN
            transmitTable.destination = Device.CUTDOWN
            transmitTable.body = cutdown_body_bytes
            transmitTable.save()

            # cutdown_packet_type = Type.CUTDOWN
            # cutdown_destination = Device.CUTDOWN
            #
            # cursor.execute(
            #     """
            #     INSERT INTO eos_schema.transmit_table (cutdown_packet_type, packet_sender, packet_priority, cutdown_destination, packet_generate_time, cutdown_body_bytes)
            #     VALUES (%s,%s,%s,%s,%s,%s)
            #     """, (cutdown_packet_type, packet_sender, packet_priority, cutdown_destination, packet_generate_time, cutdown_body_bytes)
            # )
            #
            # connection.commit()

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

            # ping_packet_type = Type.PING
            # ping_destination = Device.MISC_RADIO_1
            #
            # cursor.execute(
            #     """
            #     INSERT INTO eos_schema.transmit_table (packet_type, sender, priority, destination, generate_time, body)
            #     VALUES (%s,%s,%s,%s,%s,%s)
            #     """, (ping_packet_type, packet_sender, packet_priority, ping_destination, packet_generate_time,
            #           ping_packet_bytes)
            # )
            #
            # connection.commit()
            cursor.execute("NOTIFY update;")
            connection.commit()
            return Response({'message': 'Ping command sent ', 'ack': ack}, status=status.HTTP_200_OK)

        return Response({'message': 'Invalid input or method'}, status=status.HTTP_400_BAD_REQUEST)

