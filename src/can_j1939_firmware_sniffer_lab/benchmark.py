from __future__ import annotations

from time import perf_counter

from can_j1939_firmware_sniffer_lab.serial_parser import parse_lines


def generate_large_dataset(frame_count: int) -> list[str]:
    if frame_count <= 0:
        raise ValueError("frame_count must be positive")
    lines = ["# timestamp_ms,can_id_hex,dlc,payload_hex"]
    can_ids = ["0x18F00401", "0x18FEF100", "0x0CF00322", "0x18EAFF33"]
    payloads = ["11 22 33 44 55 66 77 88", "00 10 20 30 40 50 60 70", "AA BB CC DD EE FF 00 11", "00 F0 00"]
    dlcs = [8, 8, 8, 3]
    for index in range(frame_count):
        slot = index % len(can_ids)
        lines.append(f"{index},{can_ids[slot]},{dlcs[slot]},{payloads[slot]}")
    return lines


def benchmark_parser(frame_count: int) -> dict[str, float | int]:
    started = perf_counter()
    frames = parse_lines(generate_large_dataset(frame_count))
    duration_seconds = perf_counter() - started
    return {
        "frames": len(frames),
        "duration_seconds": round(duration_seconds, 4),
        "frames_per_second": round(len(frames) / duration_seconds, 2),
    }
