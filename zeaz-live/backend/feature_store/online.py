import json

import redis

r = redis.Redis(host="localhost", decode_responses=True)


def put(tenant: str, feats: dict):
    r.set(f"feat:{tenant}", json.dumps(feats))


def get(tenant: str) -> dict:
    v = r.get(f"feat:{tenant}")
    return json.loads(v) if v else {}
