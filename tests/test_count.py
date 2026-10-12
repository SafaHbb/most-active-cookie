from datetime import date

from most_active_cookie.count import count_cookies, find_most_active


def test_count_only_target_date():
    rows = [
        {'cookie': 'A', 'timestamp': '2018-12-10T10:00:00+00:00'},
        {'cookie': 'A', 'timestamp': '2018-12-09T14:00:00+00:00'},
        {'cookie': 'B', 'timestamp': '2018-12-09T12:00:00+00:00'},
        {'cookie': 'A', 'timestamp': '2018-12-09T10:00:00+00:00'},
        {'cookie': 'C', 'timestamp': '2018-12-08T10:00:00+00:00'},
    ]

    assert count_cookies(rows, date(2018, 12, 9)) == {'A': 2, 'B': 1}


def test_count_no_matching_date():
    rows = [{'cookie': 'A', 'timestamp': '2018-12-09T10:00:00+00:00'}]

    assert count_cookies(rows, date(2020, 1, 1)) == {}


def test_count_stops_after_target_date():
    # The last row is never read, so its bad timestamp doesn't cause an error
    rows = [
        {'cookie': 'A', 'timestamp': '2018-12-09T10:00:00+00:00'},
        {'cookie': 'B', 'timestamp': '2018-12-08T10:00:00+00:00'},
        {'cookie': 'C', 'timestamp': 'bad-date'},
    ]

    assert count_cookies(rows, date(2018, 12, 9)) == {'A': 1}


def test_find_most_active_single():
    assert find_most_active({'A': 2, 'B': 1, 'C': 1}) == {'A': 2}


def test_find_most_active_tie():
    assert find_most_active({'A': 1, 'B': 1, 'C': 1}) == {'A': 1, 'B': 1, 'C': 1}


def test_find_most_active_bigger_count_later():
    assert find_most_active({'A': 1, 'B': 1, 'C': 3}) == {'C': 3}


def test_find_most_active_empty():
    assert find_most_active({}) == {}
