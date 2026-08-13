from __future__ import annotations

from can_j1939_firmware_sniffer_lab.serial_parser import parse_lines


SYNTHETIC_LINES = [
    "# timestamp_ms,can_id_hex,dlc,payload_hex",
    "100,0x18F00401,8,11 22 33 44 55 66 77 88",
    "120,0x18FEF100,8,00 10 20 30 40 50 60 70",
    "150,0x0CF00322,8,AA BB CC DD EE FF 00 11",
    "180,0x18EAFF33,3,00 F0 00",
    "210,0x18F00401,8,12 22 33 44 55 66 77 88",
]


def synthetic_frames():
    return parse_lines(SYNTHETIC_LINES)

