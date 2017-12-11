import json


def read():
    try:
        with open('tasks.json', 'rt') as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def write(tasks):
    with open('tasks.json', 'wt') as file:
        file.write(json.dumps(tasks))
