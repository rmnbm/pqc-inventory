"""Tests for cli.py."""

from pathlib import Path

import pytest

from pqc_inventory.cli import build_parser, main


def test_defaults():
    args = build_parser().parse_args(["--files", "certs"])
    assert args.tls is None
    assert args.ssh is None
    assert args.out == Path("out")
    assert args.exposure == "unknown"
    assert args.timeout == 5.0
    assert args.delay == 1.0


def test_files_is_converted_to_path():
    args = build_parser().parse_args(["--files", "certs"])
    assert isinstance(args.files, Path)


def test_timeout_is_converted_to_float():
    args = build_parser().parse_args(["--files", "certs", "--timeout", "2.5"])
    assert args.timeout == 2.5


def test_invalid_exposure_exits_with_code_2():
    with pytest.raises(SystemExit) as exc:
        build_parser().parse_args(["--exposure", "moon"])
    assert exc.value.code == 2


def test_invalid_timeout_exits_with_code_2():
    with pytest.raises(SystemExit) as exc:
        build_parser().parse_args(["--timeout", "abc"])
    assert exc.value.code == 2


def test_nothing_to_scan_returns_2(capsys):
    code = main([])
    captured = capsys.readouterr()
    assert code == 2
    assert "Nothing to scan" in captured.err


@pytest.mark.parametrize("argv", [["--files", "x"], ["--tls", "x"], ["--ssh", "x"]])
def test_single_target_is_enough(argv):
    assert main(argv) == 0


def test_version_is_printed(capsys):
    with pytest.raises(SystemExit) as exc:
        main(["--version"])
    assert exc.value.code == 0
    assert "0.1.0" in capsys.readouterr().out
