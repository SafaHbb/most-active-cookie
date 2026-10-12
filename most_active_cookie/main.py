import argparse
import csv
import sys
from datetime import date

from most_active_cookie.load import read_csv
from most_active_cookie.count import count_cookies, find_most_active


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--filename', required=True)
    parser.add_argument('-d', '--date', required=True, type=date.fromisoformat)
    args = parser.parse_args()

    try:
        rows = read_csv(args.filename)
        counts = count_cookies(rows, args.date)
        result = find_most_active(counts)

    
    except FileNotFoundError:
        print(f'File not found: {args.filename}', file=sys.stderr)
        sys.exit(1)
    except (OSError, ValueError, csv.Error) as error:
        print(f'Error: {error}', file=sys.stderr)
        sys.exit(1)

    for cookie in result:
        print(cookie)


if __name__ == '__main__':
    main()
