from dataclasses import dataclass


@dataclass
class ShadowResult:
    action: str
    expected_latency_delta: float
    expected_error_delta: float
    risk: float


class ShadowEngine:
    """No-op simulator for remediation actions using lightweight priors."""

    PRIORS = {
        "scale_api": {"lat": -0.2, "err": -0.1, "risk": 0.1},
        "restart_pods": {"lat": -0.1, "err": -0.2, "risk": 0.2},
        "rollback_deploy": {"lat": -0.15, "err": -0.3, "risk": 0.3},
        "scale_consumers": {"lat": -0.05, "err": -0.05, "risk": 0.1},
        "restart_kafka": {"lat": 0.1, "err": 0.2, "risk": 0.6},
    }

    def simulate(self, actions: list[str]) -> list[ShadowResult]:
        results = []
        for action in actions:
            prior = self.PRIORS.get(action, {"lat": 0.0, "err": 0.0, "risk": 0.5})
            results.append(
                ShadowResult(
                    action=action,
                    expected_latency_delta=prior["lat"],
                    expected_error_delta=prior["err"],
                    risk=prior["risk"],
                )
            )
        return results
