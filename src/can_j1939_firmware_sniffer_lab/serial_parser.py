from __future__ import annotations

from can_j1939_firmware_sniffer_lab.j1939 import J1939Frame, build_frame, parse_payload_hex


def parse_sniffer_line(line: str) -> J1939Frame:
    parts = [part.strip() for part in line.strip().split(",")]
    if len(parts) != 4:
        raise ValueError("Expected line format: timestamp_ms,can_id_hex,dlc,payload_hex")
    timestamp_ms = int(parts[0])
    can_id = int(parts[1], 16)
    if can_id <= 0x7FF:
        raise ValueError("Standard 11-bit CAN IDs are not accepted for J1939 sniffer lines")
    declared_dlc = int(parts[2])
    if declared_dlc < 0 or declared_dlc > 8:
        raise ValueError("DLC must be between 0 and 8")
    payload = parse_payload_hex(parts[3])
    if declared_dlc != len(payload):
        raise ValueError(f"DLC mismatch: declared {declared_dlc}, got {len(payload)} bytes")
    return build_frame(timestamp_ms, can_id, payload)


def parse_lines(lines: list[str]) -> list[J1939Frame]:
    frames: list[J1939Frame] = []
    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        frames.append(parse_sniffer_line(stripped))
    return frames

