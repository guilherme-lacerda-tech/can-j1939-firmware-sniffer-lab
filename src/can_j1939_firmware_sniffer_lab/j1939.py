from __future__ import annotations

from dataclasses import dataclass


PDU1_MAX_PF = 239


@dataclass(frozen=True)
class J1939Identifier:
    raw_id: int
    priority: int
    reserved: int
    data_page: int
    pdu_format: int
    pdu_specific: int
    source_address: int
    pgn: int
    destination_address: int | None


@dataclass(frozen=True)
class J1939Frame:
    timestamp_ms: int
    can_id: int
    priority: int
    pgn: int
    source_address: int
    destination_address: int | None
    data_length: int
    payload: bytes

    @property
    def payload_hex(self) -> str:
        return " ".join(f"{byte:02X}" for byte in self.payload)

    def to_dict(self) -> dict[str, object]:
        return {
            "timestamp_ms": self.timestamp_ms,
            "can_id": f"0x{self.can_id:08X}",
            "priority": self.priority,
            "pgn": self.pgn,
            "source_address": self.source_address,
            "destination_address": self.destination_address,
            "data_length": self.data_length,
            "payload": self.payload_hex,
        }


def parse_can_id(can_id: int) -> J1939Identifier:
    if can_id < 0 or can_id > 0x1FFFFFFF:
        raise ValueError("J1939 extended CAN ID must be between 0 and 0x1FFFFFFF")
    priority = (can_id >> 26) & 0x7
    reserved = (can_id >> 25) & 0x1
    data_page = (can_id >> 24) & 0x1
    pdu_format = (can_id >> 16) & 0xFF
    pdu_specific = (can_id >> 8) & 0xFF
    source_address = can_id & 0xFF
    if pdu_format <= PDU1_MAX_PF:
        pgn = (data_page << 16) | (pdu_format << 8)
        destination_address = pdu_specific
    else:
        pgn = (data_page << 16) | (pdu_format << 8) | pdu_specific
        destination_address = None
    return J1939Identifier(
        raw_id=can_id,
        priority=priority,
        reserved=reserved,
        data_page=data_page,
        pdu_format=pdu_format,
        pdu_specific=pdu_specific,
        source_address=source_address,
        pgn=pgn,
        destination_address=destination_address,
    )


def build_frame(timestamp_ms: int, can_id: int, payload: bytes) -> J1939Frame:
    if len(payload) > 8:
        raise ValueError("Classic CAN payload cannot exceed 8 bytes")
    identifier = parse_can_id(can_id)
    return J1939Frame(
        timestamp_ms=timestamp_ms,
        can_id=can_id,
        priority=identifier.priority,
        pgn=identifier.pgn,
        source_address=identifier.source_address,
        destination_address=identifier.destination_address,
        data_length=len(payload),
        payload=payload,
    )


def parse_payload_hex(payload: str) -> bytes:
    cleaned = payload.replace(",", " ").replace("-", " ").strip()
    if not cleaned:
        return b""
    try:
        values = [int(part, 16) for part in cleaned.split()]
    except ValueError as exc:
        raise ValueError(f"Invalid payload hex: {payload}") from exc
    if any(value < 0 or value > 0xFF for value in values):
        raise ValueError("Payload bytes must be between 00 and FF")
    return bytes(values)

