class PacketFormatError(Exception):
    pass


class TransmitHeaderFormatError(PacketFormatError):
    pass


class DataHeaderFormatError(PacketFormatError):
    pass
