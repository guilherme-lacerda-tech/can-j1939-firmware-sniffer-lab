from __future__ import annotations

from collections.abc import Iterable

from can_j1939_firmware_sniffer_lab.j1939 import J1939Frame


def filter_frames(
    frames: Iterable[J1939Frame],
    *,
    pgn: int | None = None,
    source: int | None = None,
    destination: int | None = None,
) -> list[J1939Frame]:
    result: list[J1939Frame] = []
    for frame in frames:
        if pgn is not None and frame.pgn != pgn:
            continue
        if source is not None and frame.source_address != source:
            continue
        if destination is not None and frame.destination_address != destination:
            continue
        result.append(frame)
    return result


def frame_statistics(frames: Iterable[J1939Frame]) -> dict[str, object]:
    total = 0
    by_pgn: dict[str, int] = {}
    by_source: dict[str, int] = {}
    for frame in frames:
        total += 1
        pgn_key = str(frame.pgn)
        source_key = str(frame.source_address)
        by_pgn[pgn_key] = by_pgn.get(pgn_key, 0) + 1
        by_source[source_key] = by_source.get(source_key, 0) + 1
    return {"total": total, "by_pgn": by_pgn, "by_source": by_source}

