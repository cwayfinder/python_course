import multiprocessing
import urllib.request


def req(url):
    r = urllib.request.urlopen(url)
    return len(r.read())


p = multiprocessing.Pool(5)

print(p.map(req, ['http://example.com'] * 50))
