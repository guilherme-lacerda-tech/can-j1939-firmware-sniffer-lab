import json

from can_j1939_firmware_sniffer_lab import cli
from can_j1939_firmware_sniffer_lab.exporters import write_csv, write_json
from can_j1939_firmware_sniffer_lab.simulation import synthetic_frames


def test_export_json_and_csv(tmp_path) -> None:
    frames = synthetic_frames()
    json_path = write_json(frames, tmp_path / "frames.json")
    csv_path = write_csv(frames, tmp_path / "frames.csv")
    assert json.loads(json_path.read_text(encoding="utf-8"))[0]["pgn"] == 61444
    assert "timestamp_ms,can_id,priority" in csv_path.read_text(encoding="utf-8")


def test_export_errors_surface_invalid_path(tmp_path) -> None:
    directory = tmp_path / "directory"
    directory.mkdir()
    try:
        write_json(synthetic_frames(), directory)
    except OSError as exc:
        assert exc
    else:
        raise AssertionError("expected export to a directory path to fail")


def test_cli_simulate_filters_and_exports(tmp_path, capsys) -> None:
    json_path = tmp_path / "filtered.json"
    assert cli.main(["simulate", "--pgn", "61444", "--json", str(json_path)]) == 0
    printed = json.loads(capsys.readouterr().out)
    assert printed["statistics"]["total"] == 2
    assert json_path.exists()


def test_cli_parse_file(tmp_path, capsys) -> None:
    path = tmp_path / "frames.txt"
    path.write_text("100,0x18F00401,8,11 22 33 44 55 66 77 88\n", encoding="utf-8")
    assert cli.main(["parse-file", str(path), "--source", "1"]) == 0
    printed = json.loads(capsys.readouterr().out)
    assert printed["statistics"]["total"] == 1

