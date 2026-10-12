import csv


def read_csv(path):
    with open(path, encoding='utf-8-sig', newline='') as file:
        reader = csv.DictReader(file)

        columns = reader.fieldnames or []
        if 'cookie' not in columns or 'timestamp' not in columns:
            raise ValueError('CSV must have cookie and timestamp columns')

        for row in reader:
            if None in row or not row['cookie'] or not row['timestamp']:
                raise ValueError(f'Invalid CSV row on line {reader.line_num}')

            yield row
