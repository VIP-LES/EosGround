import pytest

import EosLib
import EosLib.packet.definitions as definitions

from datetime import datetime
from EosLib.packet.packet import TransmitHeader, DataHeader, Packet, PacketFormatError
from EosLib.packet.exceptions import DataHeaderFormatError, TransmitHeaderFormatError


def get_valid_packet():
    transmit_header = TransmitHeader(0, datetime.now())
    data_header = DataHeader(definitions.Device.GPS,
                             definitions.Type.TELEMETRY,
                             definitions.Priority.TELEMETRY,
                             definitions.Device.GPS,
                             datetime.now())

    return Packet(bytes("Hello World", 'utf-8'), data_header, transmit_header)


def test_minimal_constructor():
    data_header = DataHeader(EosLib.Device.GPS)
    packet = Packet(b'Hello, World', data_header)
    packet.encode()


def test_validate_good_transmit_header():
    test_packet = get_valid_packet()
    assert test_packet.transmit_header.validate_transmit_header()


def test_validate_bad_transmit_header_num():
    test_packet = get_valid_packet()
    test_packet.transmit_header.send_seq_num = None
    with pytest.raises(TransmitHeaderFormatError):
        test_packet.transmit_header.validate_transmit_header()


def test_validate_bad_transmit_header_time():
    test_packet = get_valid_packet()
    test_packet.transmit_header.send_time = None
    with pytest.raises(TransmitHeaderFormatError):
        test_packet.transmit_header.validate_transmit_header()


def test_validate_good_data_header():
    test_packet = get_valid_packet()
    assert test_packet.data_header.validate_data_header()


def test_validate_bad_data_header_type():
    test_packet = get_valid_packet()
    test_packet.data_header.data_type = None
    with pytest.raises(DataHeaderFormatError):
        test_packet.data_header.validate_data_header()


def test_validate_bad_data_sender():
    test_packet = get_valid_packet()
    test_packet.data_header.sender = 256
    with pytest.raises(DataHeaderFormatError):
        test_packet.data_header.validate_data_header()


def test_validate_bad_data_priority():
    test_packet = get_valid_packet()
    test_packet.data_header.priority = 256
    with pytest.raises(DataHeaderFormatError):
        test_packet.data_header.validate_data_header()


def test_validate_bad_destination():
    test_packet = get_valid_packet()
    test_packet.data_header.destination = 256
    with pytest.raises(DataHeaderFormatError):
        test_packet.data_header.validate_data_header()


def test_validate_bad_data_time():
    test_packet = get_valid_packet()
    test_packet.data_header.generate_time = None
    with pytest.raises(DataHeaderFormatError):
        test_packet.data_header.validate_data_header()


def test_validate_body_only_packet():
    model_packet = get_valid_packet()

    model_packet.transmit_header = None
    model_packet.data_header = None

    with pytest.raises(PacketFormatError):
        model_packet.encode()


def test_validate_empty_body_packet():
    model_packet = get_valid_packet()
    model_packet.body = None

    with pytest.raises(PacketFormatError):
        model_packet.encode()


def test_encode_decode_packet():
    model_packet = get_valid_packet()
    test_packet = get_valid_packet()

    encoded_packet = test_packet.encode()
    decoded_packet = Packet.decode(encoded_packet)

    decoded_packet.encode()
    assert model_packet == decoded_packet


def test_encode_decode_data_only_packet():
    model_packet = get_valid_packet()
    test_packet = get_valid_packet()

    model_packet.transmit_header = None
    test_packet.transmit_header = None

    encoded_packet = test_packet.encode()
    decoded_packet = Packet.decode(encoded_packet)

    decoded_packet.encode()
    assert model_packet == decoded_packet


def test_body_too_large():
    test_packet = get_valid_packet()
    test_packet.body = bytes(Packet.radio_body_max_bytes + 1)
    with pytest.raises(PacketFormatError):
        test_packet.encode()


def test_illegal_body_type():
    test_packet = get_valid_packet()
    test_packet.body = "Hello World"

    with pytest.raises(PacketFormatError):
        test_packet.encode()


def test_allow_large_body_no_transmit():
    test_packet = get_valid_packet()
    test_packet.body = bytes(Packet.radio_body_max_bytes + 1)
    test_packet.data_header.priority = definitions.Priority.NO_TRANSMIT

    assert test_packet.encode()


def test_max_body_size():
    test_packet = get_valid_packet()
    test_packet.body = bytes(Packet.radio_body_max_bytes)
    assert test_packet.encode()


def test_standalone_data_header_validate():
    test_header = bytearray(10)

    with pytest.raises(PacketFormatError):
        DataHeader.decode(test_header)


def test_standalone_transmit_header_validate():
    test_header = bytearray(10)

    with pytest.raises(PacketFormatError):
        TransmitHeader.decode(test_header)


def test_encode_and_decode_string():
    test_packet = get_valid_packet()
    test_string = test_packet.encode_to_string()
    decoded_packet = Packet.decode_from_string(test_string)

    decoded_packet.encode()
    assert decoded_packet == test_packet


def test_encode_string_no_tx_header():
    test_packet = get_valid_packet()
    test_packet.transmit_header = None

    test_string = test_packet.encode_to_string()
    decoded_packet = Packet.decode_from_string(test_string)

    decoded_packet.encode()
    assert decoded_packet == test_packet


def test_old_data_header_version():
    test_packet = get_valid_packet()
    test_packet.transmit_header = None

    encoded_bytes = test_packet.encode()
    old_encoded_bytes = b'\x02' + encoded_bytes[1:]

    with pytest.raises(PacketFormatError):
        Packet.decode(old_encoded_bytes)


def test_packet_print_two_headers():
    test_packet = get_valid_packet()

    # Set the times to non-now times to be sure they aren't being overridden by datetime.now()
    test_packet.data_header.generate_time = datetime.fromisoformat("2001-01-07 01:23:45.000")
    test_packet.transmit_header.send_time = datetime.fromisoformat("2002-01-07 01:23:45.000")

    expected_string = "Transmit Header:\n" \
                      "\tSend time:2002-01-07 01:23:45\n" \
                      "\tSequence number: 0\n" \
                      "Data Header:\n" \
                      "\tSender: GPS\n" \
                      "\tData type: TELEMETRY\n" \
                      "\tPriority: TELEMETRY\n" \
                      "\tDestination: GPS\n" \
                      "\tGenerate Time: 2001-01-07 01:23:45\n" \
                      "Body: b'Hello World'"

    assert expected_string == test_packet.__str__()


def test_packet_data_header_only():
    test_packet = get_valid_packet()

    # Set the times to non-now times to be sure they aren't being overridden by datetime.now()
    test_packet.data_header.generate_time = datetime.fromisoformat("2001-01-07 01:23:45.000")

    test_packet.transmit_header = None

    expected_string = "No transmit header\n" \
                      "Data Header:\n" \
                      "\tSender: GPS\n" \
                      "\tData type: TELEMETRY\n" \
                      "\tPriority: TELEMETRY\n" \
                      "\tDestination: GPS\n" \
                      "\tGenerate Time: 2001-01-07 01:23:45\n" \
                      "Body: b'Hello World'"

    assert expected_string == test_packet.__str__()


def test_packet_no_headers():
    # This shouldn't ever happen, but is a possible state so we should test for it.
    test_packet = get_valid_packet()

    test_packet.data_header = None
    test_packet.transmit_header = None

    expected_string = "No transmit header\n" \
                      "No data header\n" \
                      "Body: b'Hello World'"

    assert expected_string == test_packet.__str__()


def test_packet_print_no_body():
    test_packet = get_valid_packet()

    # Set the times to non-now times to be sure they aren't being overridden by datetime.now()
    test_packet.data_header.generate_time = datetime.fromisoformat("2001-01-07 01:23:45.000")
    test_packet.transmit_header.send_time = datetime.fromisoformat("2002-01-07 01:23:45.000")

    test_packet.body = None

    expected_string = "Transmit Header:\n" \
                      "\tSend time:2002-01-07 01:23:45\n" \
                      "\tSequence number: 0\n" \
                      "Data Header:\n" \
                      "\tSender: GPS\n" \
                      "\tData type: TELEMETRY\n" \
                      "\tPriority: TELEMETRY\n" \
                      "\tDestination: GPS\n" \
                      "\tGenerate Time: 2001-01-07 01:23:45\n" \
                      "No body"

    assert expected_string == test_packet.__str__()
