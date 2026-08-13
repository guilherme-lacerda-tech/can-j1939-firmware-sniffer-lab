from __future__ import annotations

import argparse
import json
from pathlib import Path

from can_j1939_firmware_sniffer_lab.exporters import write_csv, write_json
from can_j1939_firmware_sniffer_lab.filtering import filter_frames, frame_statistics
from can_j1939_firmware_sniffer_lab.serial_parser import parse_lines
from can_j1939_firmware_sniffer_lab.simulation import synthetic_frames


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="j1939-sniffer-lab",
        description="Parse, filter and export synthetic or captured J1939 sniffer frames.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    simulate = subparsers.add_parser("simulate", help="Analyze the built-in synthetic frame dataset.")
    add_common_args(simulate)
    simulate.set_defaults(func=handle_simulate)

    parse = subparsers.add_parser("parse-file", help="Parse a sniffer CSV-like text file.")
    parse.add_argument("path", type=Path)
    add_common_args(parse)
    parse.set_defaults(func=handle_parse_file)
    return parser


def add_common_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--pgn", type=lambda value: int(value, 0))
    parser.add_argument("--source", type=lambda value: int(value, 0))
    parser.add_argument("--destination", type=lambda value: int(value, 0))
    parser.add_argument("--json", type=Path, dest="json_path")
    parser.add_argument("--csv", type=Path, dest="csv_path")


def emit(frames, args: argparse.Namespace) -> int:
    filtered = filter_frames(frames, pgn=args.pgn, source=args.source, destination=args.destination)
    if args.json_path:
        write_json(filtered, args.json_path)
    if args.csv_path:
        write_csv(filtered, args.csv_path)
    print(json.dumps({"statistics": frame_statistics(filtered), "frames": [frame.to_dict() for frame in filtered]}, indent=2, sort_keys=True))
    return 0


def handle_simulate(args: argparse.Namespace) -> int:
    return emit(synthetic_frames(), args)


def handle_parse_file(args: argparse.Namespace) -> int:
    lines = args.path.read_text(encoding="utf-8").splitlines()
    return emit(parse_lines(lines), args)


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())

