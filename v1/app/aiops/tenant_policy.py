from collections import defaultdict

from app.aiops.bandit_ts import LinTS


class TenantPolicies:
    def __init__(self, d: int = 8):
        self.models = defaultdict(lambda: LinTS(d=d))

    def get(self, tenant_id: str) -> LinTS:
        return self.models[tenant_id]

    def snapshot(self):
        return None

    def load(self):
        return None
