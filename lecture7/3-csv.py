import csv


class CsvContainer:
    def __init__(self, file_name, field_names):
        self.field_names = field_names
        self.file_name = file_name

    def append(self, value):
        rows = self.read_rows()
        rows.append(value)
        self.write_rows(rows)

    def get_value(self, row_number, col_name):
        rows = self.read_rows()
        return rows[row_number][col_name]

    def set_value(self, row_number, col_name, value):
        rows = self.read_rows()
        rows[row_number][col_name] = value
        self.write_rows(rows)

    def read_rows(self):
        with open(self.file_name, 'rt') as file:
            return list(csv.DictReader(file))

    def write_rows(self, rows):
        with open(self.file_name, 'wt') as file:
            writer = csv.DictWriter(file, self.field_names)
            writer.writeheader()
            for row in rows:
                writer.writerow(row)


c = CsvContainer('lines.csv', ('name', 'amount', 'price'))
c.append({'name': 'wheat', 'amount': 3, 'price': 4.2})
c.append({'name': 'fish', 'amount': 4, 'price': 8.2})
c.append({'name': 'meat', 'amount': 1, 'price': 11.2})
c.set_value(1, 'amount', 55)
