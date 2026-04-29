import json

try:
    import redis
except Exception:  # pragma: no cover
    redis = None


class OnlineStore:
    def __init__(self):
        self.db = redis.Redis(host="redis", port=6379, decode_responses=True) if redis else None

    def put(self, tenant: str, feats: dict, ttl: int = 60):
        if not self.db:
            return
        self.db.setex(f"fs:{tenant}", ttl, json.dumps(feats))

    def get(self, tenant: str):
        if not self.db:
            return None
        value = self.db.get(f"fs:{tenant}")
        return json.loads(value) if value else None
