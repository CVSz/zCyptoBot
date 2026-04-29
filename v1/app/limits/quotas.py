from collections import defaultdict

from app.tenancy.context import get_tenant


class Quota:
    def __init__(self, daily_limit: int = 10000):
        self.limit = daily_limit
        self.usage = defaultdict(int)

    def consume(self, n: int = 1) -> bool:
        tenant = get_tenant()
        if self.usage[tenant] + n > self.limit:
            return False
        self.usage[tenant] += n
        return True
