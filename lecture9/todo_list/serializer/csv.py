import csv


def read():
    try:
        with open('tasks.csv', 'rt') as file:
            return list(csv.DictReader(file))
    except FileNotFoundError:
        return []


def write(tasks):
    with open('tasks.csv', 'wt') as file:
        writer = csv.DictWriter(file, list(tasks[0].keys()))
        writer.writeheader()
        for task in tasks:
            writer.writerow(task)
