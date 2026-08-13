import pytest

from can_j1939_firmware_sniffer_lab.j1939 import build_frame, parse_can_id, parse_payload_hex


def test_parse_pdu2_identifier() -> None:
    identifier = parse_can_id(0x18F00401)
    assert identifier.priority == 6
    assert identifier.pgn == 61444
    assert identifier.source_address == 0x01
    assert identifier.destination_address is None


def test_parse_pdu1_identifier_with_destination() -> None:
    identifier = parse_can_id(0x18EAFF33)
    assert identifier.pgn == 59904
    assert identifier.destination_address == 0xFF
    assert identifier.source_address == 0x33


def test_reject_invalid_can_id() -> None:
    with pytest.raises(ValueError, match="extended CAN ID"):
        parse_can_id(0x3FFFFFFF)


def test_build_frame_rejects_too_long_payload() -> None:
    with pytest.raises(ValueError, match="cannot exceed 8"):
        build_frame(1, 0x18F00401, bytes(range(9)))


def test_payload_hex_parser() -> None:
    assert parse_payload_hex("AA BB-CC,DD") == bytes([0xAA, 0xBB, 0xCC, 0xDD])
    assert parse_payload_hex("") == b""
    with pytest.raises(ValueError, match="Invalid payload"):
        parse_payload_hex("not_hex")

