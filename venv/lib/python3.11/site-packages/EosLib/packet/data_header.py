import math
import struct

from datetime import datetime
from EosLib.packet import definitions
from EosLib.packet.definitions import HeaderPreamble, old_data_headers
from EosLib.packet.exceptions import PacketFormatError, DataHeaderFormatError


class DataHeader:

    data_header_struct_format_string = "!" \
                                       "B" \
                                       "B" \
                                       "B" \
                                       "B" \
                                       "B" \
                                       "d"

    def __init__(self,
                 sender: definitions.Device,
                 data_type: definitions.Type = definitions.Type.NO_TYPE,
                 priority: definitions.Priority = definitions.Priority.NO_TRANSMIT,
                 destination: definitions.Device = definitions.Device.NO_DEVICE,
                 generate_time: datetime = None
                 ):
        if generate_time is None:
            generate_time = datetime.now()
        self.sender = sender
        self.data_type = data_type
        self.priority = priority
        self.destination = destination
        self.generate_time = generate_time

    def __eq__(self, other):
        """ Compares two transmit headers for value equality

        :param other: the other header to be compared
        :return:
        """
        return (self.priority == other.priority and
                self.data_type == other.data_type and
                self.sender == other.sender and
                self.destination == other.destination and
                math.isclose(self.generate_time.timestamp(), other.generate_time.timestamp()))

    # TODO: Expand validation criteria
    def validate_data_header(self):
        """ Checks that all fields in the TransmitHeader object are valid and throws an exception if they aren't.

        :return: True if valid
        """
        if not isinstance(self.sender, int) or not 0 <= self.sender <= 255 or self.sender == \
                definitions.Device.NO_DEVICE:
            raise DataHeaderFormatError("Invalid Sender")

        if not isinstance(self.data_type, int) or not 0 <= self.data_type <= 255:
            raise DataHeaderFormatError("Invalid Type")

        if not isinstance(self.priority, int) or not 0 <= self.priority <= 255:
            raise DataHeaderFormatError("Invalid Priority")

        if not isinstance(self.destination, int) or not 0 <= self.destination <= 255:
            raise DataHeaderFormatError("Invalid Destination")

        if not isinstance(self.generate_time, datetime):
            raise DataHeaderFormatError("Invalid Generate Time")

        return True

    def encode(self):
        """ Checks that the header is valid and returns a bytes object if it is.

        :return: A bytes object containing the encoded header
        """
        self.validate_data_header()
        return struct.pack(DataHeader.data_header_struct_format_string,
                           HeaderPreamble.DATA,
                           self.sender,
                           self.data_type,
                           self.priority,
                           self.destination,
                           self.generate_time.timestamp())

    def encode_to_string(self):
        """ Validates the data header and converts it to a comma separated string

        :return: String encoded data header
        """
        self.validate_data_header()
        return "{sender}, {data_type}, {priority}, {destination}, " \
               "{generate_time}".format(sender=self.sender,
                                        data_type=self.data_type,
                                        priority=self.priority,
                                        destination=self.destination,
                                        generate_time=self.generate_time.isoformat())

    @staticmethod
    def decode(header_bytes: bytes):
        """Checks if the given bytes start with a DataHeader and, if so, decodes it.

        :param header_bytes: The bytes containing a data header at the front
        :return: Data header bytes format
        """
        if header_bytes[0] in old_data_headers:
            raise PacketFormatError("Created by an incompatible version of EosLib")
        elif header_bytes[0] != HeaderPreamble.DATA:
            raise PacketFormatError("Not a valid data header")

        unpacked = struct.unpack(DataHeader.data_header_struct_format_string, header_bytes)
        decoded_header = DataHeader(unpacked[1], unpacked[2], unpacked[3], unpacked[4],
                                    datetime.fromtimestamp(unpacked[5]))
        return decoded_header
