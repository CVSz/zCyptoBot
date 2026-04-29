from dataclasses import dataclass


@dataclass
class SLO:
    latency_ms_p95: float
    error_rate: float
    budget: float


class SLOPlanner:
    COST = {
        "scale_api": 0.2,
        "restart_pods": 0.1,
        "rollback_deploy": 0.3,
        "scale_consumers": 0.2,
        "restart_kafka": 0.5,
    }

    def choose(self, shadow_results, slo: SLO) -> list[str]:
        scored = []
        for result in shadow_results:
            cost = self.COST.get(result.action, 0.2)
            improvement = (-result.expected_latency_delta) + (-result.expected_error_delta)
            budget_penalty = 1.0 - slo.budget
            score = improvement - (result.risk + cost + budget_penalty)
            scored.append((score, result.action))

        scored.sort(reverse=True)
        return [action for _, action in scored[:2]]
