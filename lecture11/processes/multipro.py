import multiprocessing


def hello():
    print('Hello!')


for _ in range(10):
    p = multiprocessing.Process(target=hello)
    p.start()