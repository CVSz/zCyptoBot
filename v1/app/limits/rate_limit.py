import time
from collections import defaultdict

from app.tenancy.context import get_tenant

WINDOW = 1.0
MAX_REQ = 20


class RateLimiter:
    def __init__(self):
        self.bucket = defaultdict(list)

    def allow(self) -> bool:
        tenant = get_tenant()
        now = time.time()
        arr = self.bucket[tenant]
        self.bucket[tenant] = [x for x in arr if now - x < WINDOW]
        if len(self.bucket[tenant]) >= MAX_REQ:
            return False
        self.bucket[tenant].append(now)
        return True
