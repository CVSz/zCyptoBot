import time

try:
    import redis
except Exception:  # pragma: no cover
    redis = None

_client = redis.Redis(host="redis", port=6379, decode_responses=True) if redis else None


class Quorum:
    def __init__(self, regions=("A", "B"), k=2, ttl=30):
        self.regions = regions
        self.k = k
        self.ttl = ttl

    def vote(self, action: str, region: str):
        if not _client:
            return
        key = f"q:{action}"
        _client.hset(key, region, int(time.time()))
        _client.expire(key, self.ttl)

    def approved(self, action: str):
        if not _client:
            return False
        votes = _client.hkeys(f"q:{action}")
        return len(votes) >= self.k
