import threading


def hello(index):
    print('Hello!', index)


for i in range(10):
    t = threading.Thread(target=hello, args=(i,))
    t.start()
