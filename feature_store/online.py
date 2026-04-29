import json

import redis

r = redis.Redis(decode_responses=True)


def put(k, v):
    r.set(k, json.dumps(v))


def get(k):
    return json.loads(r.get(k) or "{}")
