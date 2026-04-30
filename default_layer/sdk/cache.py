CACHE = {}


def get(k):
    return CACHE.get(k)


def set(k, v, ttl=60):
    CACHE[k] = v
