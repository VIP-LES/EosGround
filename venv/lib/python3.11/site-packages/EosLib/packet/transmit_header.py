import math
import struct

from datetime import datetime
from EosLib.packet.definitions import HeaderPreamble, old_transmit_headers
from EosLib.packet.exceptions import TransmitHeaderFormatError


class TransmitHeader:

    transmit_header_struct_format_string = "!" \
                                           "B" \
                                           "B" \
                                           "d"

    def __init__(self,
                 send_seq_num: int,
                 send_time: datetime = None):
        """Initializes a TransmitHeader object

        :param send_seq_num: The sequence number assigned at the transmitter
        :param send_time: The time the packet is sent to the transmitter
        """
        if send_time is None:
            send_time = datetime.now()

        self.send_seq_num = send_seq_num
        self.send_time = send_time

    def __eq__(self, other):
        """ Compares two transmit headers for value equality

        :param other: the other header to be compared
        :return:
        """
        return (self.send_seq_num == other.send_seq_num and
                math.isclose(self.send_time.timestamp(), other.send_time.timestamp()))

    # TODO: Expand validation criteria
    def validate_transmit_header(self):
        """Checks that all fields in the TransmitHeader object are valid and throws an exception if any aren't.

        :return: True if valid
        """
        if not isinstance(self.send_seq_num, int) or not 0 <= self.send_seq_num <= 255:
            raise TransmitHeaderFormatError("Invalid Sequence Number")

        if not isinstance(self.send_time, datetime):
            raise TransmitHeaderFormatError("Invalid Send Time")

        return True

    def encode(self):
        """ Checks that the header is valid and returns a bytes object if it is.

        :return: A bytes object containing the encoded header
        """
        self.validate_transmit_header()
        return struct.pack(TransmitHeader.transmit_header_struct_format_string, HeaderPreamble.TRANSMIT,
                           self.send_seq_num, self.send_time.timestamp())

    def encode_to_string(self):
        """ Checks that the header is valid and returns a string if it is.

        :return: A bytes object containing the encoded header
        """
        return "{send_seq_num}, {send_time}".format(send_seq_num=self.send_seq_num,
                                                    send_time=self.send_time.isoformat())

    @staticmethod
    def decode(header_bytes: bytes):
        """Checks if the given bytes start with a TransmitHeader and, if so, decodes it.

        :param header_bytes: The bytes containing a transmit header at the front
        :return: a decoded TransmitHeader
        """
        if header_bytes[0] in old_transmit_headers:
            raise TransmitHeaderFormatError("Created by an incompatible version of EosLib")
        elif header_bytes[0] != HeaderPreamble.TRANSMIT:
            raise TransmitHeaderFormatError("Not a valid transmit header")

        unpacked = struct.unpack(TransmitHeader.transmit_header_struct_format_string, header_bytes)
        decoded_header = TransmitHeader(unpacked[1], datetime.fromtimestamp(unpacked[2]))
        return decoded_header
