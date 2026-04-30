import time

CACHE = {}


def set_kv(k, v, ttl=30):
    CACHE[k] = (v, time.time() + ttl)


def get_kv(k):
    v = CACHE.get(k)
    if not v:
        return None
    val, exp = v
    if exp < time.time():
        CACHE.pop(k, None)
        return None
    return val
