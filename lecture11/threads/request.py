import threading
import urllib.request
import queue


q = queue.Queue()


def req():
    while True:
        url = q.get()
        if url is not None:
            r = urllib.request.urlopen(url)
            print(len(r.read()))
            q.task_done()


for _ in range(5):
    t = threading.Thread(target=req)
    t.start()

for _ in range(50):
    q.put('http://example.org')

q.join()

for _ in range(5):
    q.put(None)