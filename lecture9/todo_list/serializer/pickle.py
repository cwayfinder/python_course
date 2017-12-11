import pickle


def read():
    try:
        with open('tasks.pickle', 'rb') as file:
            return pickle.load(file)
    except FileNotFoundError:
        return []


def write(tasks):
    with open('tasks.pickle', 'wb') as file:
        pickle.dump(tasks, file)
