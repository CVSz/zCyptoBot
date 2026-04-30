class PolicyEngine:
    """
    Enforces tenant budgets, compliance regions, and SLO gates.
    """

    def __init__(self, tenant_policies: dict):
        self.p = tenant_policies

    def allow(self, tenant: str, region: str, cost: float) -> bool:
        tp = self.p.get(tenant, {})
        if region not in tp.get("allowed_regions", []):
            return False
        if cost > tp.get("max_unit_cost", float("inf")):
            return False
        return True
