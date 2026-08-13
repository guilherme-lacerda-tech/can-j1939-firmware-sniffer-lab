from __future__ import annotations

import csv
import json
from pathlib import Path

from can_j1939_firmware_sniffer_lab.j1939 import J1939Frame


def write_json(frames: list[J1939Frame], path: str | Path) -> Path:
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps([frame.to_dict() for frame in frames], indent=2), encoding="utf-8")
    return output


def write_csv(frames: list[J1939Frame], path: str | Path) -> Path:
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "timestamp_ms",
                "can_id",
                "priority",
                "pgn",
                "source_address",
                "destination_address",
                "data_length",
                "payload",
            ],
        )
        writer.writeheader()
        writer.writerows(frame.to_dict() for frame in frames)
    return output

