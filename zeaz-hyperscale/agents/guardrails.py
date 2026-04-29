class Guardrails:
    def ips_dr_gate(self, score: float, baseline: float = 0.5, margin: float = 0.05) -> bool:
        return score >= (baseline + margin)

    def cost_cap(self, est_cost: float, budget: float) -> bool:
        return est_cost <= budget

    def quorum(self, approvals: int, required: int = 2) -> bool:
        return approvals >= required
