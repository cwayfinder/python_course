import threading

a = 0


def f():
    global a
    for _ in range(10000):
        a += 1


for i in range(100):
    t = threading.Thread(target=f)
    t.start()

print(a)
