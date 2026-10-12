from most_active_cookie.transform_dates import get_date


def count_cookies(rows, target_date):
    # Rows are sorted newest first, so we can stop once we pass the target date.
    counts = {}

    for row in rows:
        row_date = get_date(row['timestamp'])

        if row_date < target_date:
            break

        if row_date == target_date:
            cookie = row['cookie']

            if cookie in counts:
                counts[cookie] = counts[cookie] + 1
            else:
                counts[cookie] = 1

    return counts


def find_most_active(counts):
    most_active = {}
    max_count = 0

    for cookie, count in counts.items():
        if count > max_count:
            most_active = {}
            most_active[cookie] = count
            max_count = count

        elif count == max_count:
            most_active[cookie] = count

    return most_active
