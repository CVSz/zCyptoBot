from app.aiops.state_store import idem_key, lease, release
from app.tenancy.context import get_tenant


class Coordinator:
    def __init__(self, region_id: str):
        self.region = region_id

    def acquire(self, action: str) -> bool:
        key = f"lease:{self.region}:{action}"
        return bool(lease(key, ttl=30))

    def done(self, action: str):
        release(f"lease:{self.region}:{action}")

    def dedupe(self, action: str) -> bool:
        key = idem_key(get_tenant(), f"{self.region}:{action}")
        return bool(lease(key, ttl=30))
