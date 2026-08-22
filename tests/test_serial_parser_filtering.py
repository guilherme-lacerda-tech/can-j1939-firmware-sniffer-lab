import pytest

from can_j1939_firmware_sniffer_lab.filtering import filter_frames, frame_statistics
from can_j1939_firmware_sniffer_lab.benchmark import benchmark_parser, generate_large_dataset
from can_j1939_firmware_sniffer_lab.serial_parser import FakeSerialSource, parse_lines, parse_sniffer_line, parse_source
from can_j1939_firmware_sniffer_lab.simulation import synthetic_frames


def test_parse_sniffer_line() -> None:
    frame = parse_sniffer_line("100,0x18F00401,8,11 22 33 44 55 66 77 88")
    assert frame.timestamp_ms == 100
    assert frame.pgn == 61444
    assert frame.payload_hex == "11 22 33 44 55 66 77 88"


def test_parse_ignores_blank_and_comment_lines() -> None:
    frames = parse_lines(["", "# comment", "120,0x18FEF100,8,00 10 20 30 40 50 60 70"])
    assert len(frames) == 1
    assert frames[0].pgn == 65265


def test_malformed_line_errors() -> None:
    with pytest.raises(ValueError, match="Expected line format"):
        parse_sniffer_line("bad")
    with pytest.raises(ValueError, match="DLC mismatch"):
        parse_sniffer_line("1,0x18F00401,8,AA")
    with pytest.raises(ValueError, match="Standard 11-bit"):
        parse_sniffer_line("1,0x7FF,1,AA")
    with pytest.raises(ValueError, match="DLC"):
        parse_sniffer_line("1,0x18F00401,9,AA BB CC DD EE FF 00 11 22")


def test_filter_by_pgn_source_and_destination() -> None:
    frames = synthetic_frames()
    assert len(filter_frames(frames, pgn=61444)) == 2
    assert len(filter_frames(frames, source=0x01)) == 2
    assert len(filter_frames(frames, destination=0xFF)) == 1


def test_statistics_counts_frames() -> None:
    stats = frame_statistics(synthetic_frames())
    assert stats["total"] == 5
    assert stats["by_pgn"]["61444"] == 2


def test_filter_combinations_and_empty_dataset() -> None:
    frames = synthetic_frames()
    assert filter_frames(frames, pgn=61444, source=0x01)
    assert filter_frames(frames, pgn=61444, source=0x22) == []
    assert frame_statistics([]) == {"total": 0, "by_pgn": {}, "by_source": {}}


def test_fake_serial_source_parses_lines() -> None:
    source = FakeSerialSource(["100,0x18F00401,8,11 22 33 44 55 66 77 88"])

    assert parse_source(source)[0].pgn == 61444


def test_large_dataset_benchmark_reports_throughput() -> None:
    assert len(generate_large_dataset(25)) == 26
    result = benchmark_parser(25)
    assert result["frames"] == 25
    assert result["frames_per_second"] > 0

