"""Unit tests for the CLI runner and argument validation."""

from transit_fare.cli import run_cli


def test_cli_success_outputs_receipt(capsys):
    exit_code = run_cli(["-o", "1", "-d", "4", "-p", "student", "--peak"])
    assert exit_code == 0

    captured = capsys.readouterr()
    assert "TRANSIT FARE TICKET" in captured.out
    assert "FINAL FARE:" in captured.out
    assert "€  4.25" in captured.out
    assert captured.err == ""


def test_cli_rejects_intra_zone_travel(capsys):
    exit_code = run_cli(["-o", "2", "-d", "2"])
    assert exit_code == 1

    captured = capsys.readouterr()
    assert "Error: Intra-zone travel is not supported" in captured.err


def test_cli_rejects_out_of_bounds_zone(capsys):
    exit_code = run_cli(["-o", "1", "-d", "5"])
    assert exit_code == 1

    captured = capsys.readouterr()
    assert "Error: Destination zone must be between 1 and 4" in captured.err


def test_cli_rejects_invalid_passenger_category(capsys):
    exit_code = run_cli(["-o", "1", "-d", "2", "-p", "vip"])
    assert exit_code == 1

    captured = capsys.readouterr()
    assert "Error: Invalid passenger category 'vip'" in captured.err
