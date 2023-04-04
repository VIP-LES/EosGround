import struct
from datetime import datetime
from enum import IntEnum

from EosLib import Type
from EosLib.packet.packet import Packet


class FlightState(IntEnum):
    NOT_SET = 0
    UNKNOWN = 1
    ON_GROUND = 2
    ASCENT = 3
    DESCENT = 4


class Position:
    # Struct format is: timestamp, lat, long, speed, altitude, number of satellites, flight state
    gps_struct_string = "!" \
                        "d" \
                        "d" \
                        "d" \
                        "d" \
                        "d" \
                        "H" \
                        "B"

    def __init__(self):
        self.local_time = None
        self.timestamp = None
        self.latitude = None
        self.longitude = None
        self.altitude = None
        self.speed = None
        self.number_of_satellites = None
        self.valid = False
        self.flight_state = FlightState.NOT_SET

    # TODO: figure out a more legitimate way to check validity
    def set_validity(self):
        if (self.number_of_satellites < 4 or
                self.latitude == 0 or
                self.longitude == 0):
            self.valid = False
        else:
            self.valid = True

    @staticmethod
    def decode_position(gps_packet: Packet):
        new_position = Position()
        new_position.local_time = datetime.now()
        new_position.gps_packet = gps_packet
        if new_position.gps_packet.data_header.data_type != Type.POSITION:
            raise ValueError("Packet is not a position")

        unpacked_tuple = struct.unpack(Position.gps_struct_string, new_position.gps_packet.body)
        new_position.timestamp = unpacked_tuple[0]
        new_position.latitude = unpacked_tuple[1]
        new_position.longitude = unpacked_tuple[2]
        new_position.altitude = unpacked_tuple[3]
        new_position.speed = unpacked_tuple[4]
        new_position.number_of_satellites = unpacked_tuple[5]
        new_position.flight_state = unpacked_tuple[6]
        new_position.set_validity()

        return new_position

    @staticmethod
    def encode_position(timestamp: float, latitude: float, longitude: float, altitude: float, speed: float,
                        number_of_satellites: int, flight_state: FlightState) -> bytes:
        return struct.pack(Position.gps_struct_string, timestamp, latitude, longitude, altitude, speed,
                           number_of_satellites, flight_state)
