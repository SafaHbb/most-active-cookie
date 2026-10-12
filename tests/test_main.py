import subprocess
import sys
from pathlib import Path

import pytest

from most_active_cookie.main import main

PROJECT_DIR = Path(__file__).parent.parent
SAMPLE_LOG = PROJECT_DIR / 'cookie_log.csv'


def run(monkeypatch, *args):
    monkeypatch.setattr(sys, 'argv', ['main.py', *args])
    main()


def test_single_cookie(monkeypatch, capsys):
    run(monkeypatch, '-f', str(SAMPLE_LOG), '-d', '2018-12-09')

    assert capsys.readouterr().out == 'AtY0laUfhglK3lC7\n'


def test_tied_cookies(monkeypatch, capsys):
    run(monkeypatch, '-f', str(SAMPLE_LOG), '-d', '2018-12-08')

    assert capsys.readouterr().out == 'SAZuXPGUrfbcn5UA\n4sMM2LxV07bPJzwf\nfbcn5UAVanZf6UtG\n'


def test_no_cookies_on_date(monkeypatch, capsys):
    run(monkeypatch, '-f', str(SAMPLE_LOG), '-d', '2020-01-01')

    assert capsys.readouterr().out == ''


def test_missing_file(monkeypatch, capsys):
    with pytest.raises(SystemExit) as error:
        run(monkeypatch, '-f', 'missing.csv', '-d', '2018-12-09')

    assert error.value.code == 1
    assert 'File not found' in capsys.readouterr().err


def test_invalid_date(monkeypatch):
    with pytest.raises(SystemExit) as error:
        run(monkeypatch, '-f', str(SAMPLE_LOG), '-d', '09-12-2018')

    assert error.value.code == 2


def test_missing_required_argument(monkeypatch):
    with pytest.raises(SystemExit) as error:
        run(monkeypatch, '-d', '2018-12-09')

    assert error.value.code == 2


def test_invalid_timestamp_in_file(tmp_path, monkeypatch, capsys):
    path = tmp_path / 'log.csv'
    path.write_text('cookie,timestamp\nA,bad-date\n')

    with pytest.raises(SystemExit) as error:
        run(monkeypatch, '-f', str(path), '-d', '2018-12-09')

    assert error.value.code == 1
    assert 'Error:' in capsys.readouterr().err


def test_cli_subprocess():
    result = subprocess.run(
        [sys.executable, '-m', 'most_active_cookie.main', '-f', str(SAMPLE_LOG), '-d', '2018-12-09'],
        capture_output=True,
        text=True,
        cwd=PROJECT_DIR,
    )

    assert result.returncode == 0
    assert result.stdout == 'AtY0laUfhglK3lC7\n'
    assert result.stderr == ''
