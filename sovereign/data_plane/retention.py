import time


def ttl_expire(records, ttl_sec: int):
    now = time.time()
    return [r for r in records if (now - r["ts"]) < ttl_sec]
