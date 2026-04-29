from collections import defaultdict

from app.aiops.bandit_ts_ns import LinTS_NS


class HierarchicalTS:
    def __init__(self, d: int = 8):
        self.global_model = LinTS_NS(d=d)
        self.tenants = defaultdict(lambda: LinTS_NS(d=d))

    def select(self, tenant_id: str, x):
        tenant_action = self.tenants[tenant_id].select(x)
        global_action = self.global_model.select(x)
        return tenant_action or global_action

    def update(self, tenant_id: str, action: str, x, reward: float):
        self.tenants[tenant_id].update(action, x, reward)
        self.global_model.update(action, x, reward)
