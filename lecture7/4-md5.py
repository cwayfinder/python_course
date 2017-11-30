import hashlib


def has_collisions(l):
    hashes = set()
    for idx, item in enumerate(l):
        hashes.add(hashlib.md5(item.encode('utf-8')).hexdigest())
        if len(hashes) <= idx:
            return True
    return False


print(has_collisions(['abc', 'abf', 'fff']))
print(has_collisions(['abc', 'abf', 'fff', 'fff']))
