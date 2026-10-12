from datetime import date

import pytest

from most_active_cookie.transform_dates import get_date


def test_get_date():
    assert get_date('2018-12-09T14:19:00+00:00') == date(2018, 12, 9)


def test_get_date_other_timezone():
    # 01:00 at +02:00 is 23:00 UTC on the previous day
    assert get_date('2018-12-10T01:00:00+02:00') == date(2018, 12, 9)


def test_get_date_day_boundaries():
    assert get_date('2018-12-09T00:00:00+00:00') == date(2018, 12, 9)
    assert get_date('2018-12-09T23:59:59+00:00') == date(2018, 12, 9)


def test_timestamp_without_timezone():
    with pytest.raises(ValueError, match='timezone'):
        get_date('2018-12-09T14:19:00')


def test_invalid_timestamp():
    with pytest.raises(ValueError):
        get_date('not-a-date')
