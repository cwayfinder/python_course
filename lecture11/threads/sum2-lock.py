import threading

a = 0
l = threading.Lock()


def f():
    global a
    for _ in range(10000):
        l.acquire()
        a += 1
        l.release()


ts = []
for _ in range(100):
    t = threading.Thread(target=f)
    t.start()
    ts.append(t)

for t in ts:
    t.join()

print(a)
