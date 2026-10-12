import pytest

from most_active_cookie.load import read_csv


def test_read_csv(tmp_path):
    path = tmp_path / 'log.csv'
    path.write_text(
        'cookie,timestamp\n'
        'AtY0laUfhglK3lC7,2018-12-09T14:19:00+00:00\n'
        'SAZuXPGUrfbcn5UA,2018-12-09T10:13:00+00:00\n'
    )

    rows = list(read_csv(path))

    assert rows == [
        {'cookie': 'AtY0laUfhglK3lC7', 'timestamp': '2018-12-09T14:19:00+00:00'},
        {'cookie': 'SAZuXPGUrfbcn5UA', 'timestamp': '2018-12-09T10:13:00+00:00'},
    ]


def test_read_csv_with_bom(tmp_path):
    path = tmp_path / 'log.csv'
    path.write_text('cookie,timestamp\nA,2018-12-09T14:19:00+00:00\n', encoding='utf-8-sig')

    rows = list(read_csv(path))

    assert rows[0]['cookie'] == 'A'


def test_extra_column_is_allowed(tmp_path):
    path = tmp_path / 'log.csv'
    path.write_text('cookie,timestamp,country\nA,2018-12-09T14:19:00+00:00,UK\n')

    rows = list(read_csv(path))

    assert rows[0]['cookie'] == 'A'


def test_empty_file(tmp_path):
    path = tmp_path / 'empty.csv'
    path.write_text('')

    with pytest.raises(ValueError, match='columns'):
        list(read_csv(path))


def test_missing_column(tmp_path):
    path = tmp_path / 'log.csv'
    path.write_text('cookie\nA\n')

    with pytest.raises(ValueError, match='columns'):
        list(read_csv(path))


def test_invalid_row_shows_line_number(tmp_path):
    path = tmp_path / 'log.csv'
    path.write_text(
        'cookie,timestamp\n'
        'A,2018-12-09T14:19:00+00:00\n'
        'B\n'
    )

    with pytest.raises(ValueError, match='line 3'):
        list(read_csv(path))


def test_header_only_file(tmp_path):
    path = tmp_path / 'log.csv'
    path.write_text('cookie,timestamp\n')

    assert list(read_csv(path)) == []
