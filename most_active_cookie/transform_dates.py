from datetime import datetime, timezone


def get_date(timestamp):
    parsed_time = datetime.fromisoformat(timestamp)

    if parsed_time.tzinfo is None:
        raise ValueError('Timestamp must include timezone')

    return parsed_time.astimezone(timezone.utc).date()
