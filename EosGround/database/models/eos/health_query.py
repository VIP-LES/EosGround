from abc import abstractmethod
from dataclasses import dataclass
from enum import IntEnum, unique
from typing_extensions import Self
import struct

from EosLib.device import Device
from EosLib.format.base_format import BaseFormat
from EosLib.format.definitions import Type

@unique
class QueryType(IntEnum):
    DEVICE = 0
    DEVICE_HISTORY = 1
    LOGS = 2
@dataclass
class HealthQuery(BaseFormat):

    def __init__(self, device_id: Device, query_type: QueryType):
        self.device_id = device_id
        self.query_type = query_type
        self.valid = self.get_validity()

    @staticmethod
    def get_format_string(self) -> str:
        return "!" \
               "B" \
               "B"

    @staticmethod
    def _i_promise_all_abstract_methods_are_implemented() -> bool:
        """ This method exists because if you use a dataclass-based format ABC gets mad because it can't figure out
           that the dataclass implements __init__, __eq__, etc.


           :return: True if isabstract check should be bypassed, otherwise False
       """
        return True

    @staticmethod
    @abstractmethod
    def get_format_type() -> Type:
        return Type.HEALTH_QUERY
        # raise NotImplementedError

    @abstractmethod
    def encode(self) -> bytes:
        return struct.pack(self.get_format_string(),
                           self.device_id,
                           self.query_type
                           )
        # raise NotImplementedError

    @classmethod
    @abstractmethod
    def decode(cls, data: bytes) -> Self:
        unpacked_data = struct.unpack(cls.get_format_string(), data)
        return HealthQuery(unpacked_data[0], unpacked_data[1])
        # raise NotImplementedError

    @abstractmethod
    def get_validity(self) -> bool:
        return (
                0 <= self.device_id <= len(Device)
                and 0 <= self.query_type <= len(QueryType)
        )
        # raise NotImplementedError
