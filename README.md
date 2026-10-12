# Most Active Cookie

Finds the most active cookie(s) for a given UTC date from a CSV log file.

## Requirements

Python 3.10+

## Setup

```bash
python -m venv .venv
source .venv/bin/activate        # on Windows: .venv\Scripts\activate
pip install -e ".[test]"
```

## Usage

After installation:

```bash
most_active_cookie -f cookie_log.csv -d 2018-12-09
```

Or run directly:

```bash
python -m most_active_cookie.main -f cookie_log.csv -d 2018-12-09
```

## Tests

```bash
python -m pytest
```

## Notes

- Dates are compared in UTC.
- If multiple cookies have the highest count, all are printed.
- If no cookies match the date, nothing is printed.
- The file is assumed to be sorted newest first, so reading stops once it passes the requested date.
- Extra columns in the CSV are ignored, but `cookie` and `timestamp` are required.
- Invalid files and timestamps print an error message and exit with code 1.
