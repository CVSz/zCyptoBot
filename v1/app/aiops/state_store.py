import hashlib
import time

import redis

r = redis.Redis(host="redis", port=6379, decode_responses=True)


def lease(key: str, ttl: int = 30):
    value = str(time.time())
    return r.set(key, value, nx=True, ex=ttl)


def release(key: str):
    r.delete(key)


def idem_key(tenant: str, action: str, window_s: int = 30) -> str:
    slot = int(time.time() // window_s)
    raw = f"{tenant}:{action}:{slot}"
    return "idem:" + hashlib.sha256(raw.encode()).hexdigest()
