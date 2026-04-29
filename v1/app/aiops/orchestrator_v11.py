from app.aiops.agents.availability import AvailabilityAgent
from app.aiops.agents.latency import LatencyAgent
from app.aiops.agents.region import RegionAgent
from app.aiops.negotiation import NegotiationEngine
from app.aiops.rewrite import RewriteEngine
from app.aiops.scaler_cloud import CloudScaler


class AIOpsV11:
    def __init__(self, agents=None):
        self.neg = NegotiationEngine(agents or [LatencyAgent(), RegionAgent(), AvailabilityAgent()])
        self.rewrite = RewriteEngine()
        self.scale = CloudScaler()

    def _gates_passed(self, state: dict) -> bool:
        return all(
            [
                state.get("shadow_pass", False),
                state.get("simulator_pass", False),
                state.get("ips_dr_pass", False),
                state.get("quorum_ok", False),
                state.get("canary_ready", False),
            ]
        )

    def step(self, state: dict):
        if state.get("kill_switch", False):
            return {"action": "hold", "reason": "kill_switch"}

        action = self.neg.negotiate(state)
        result = {"action": action}

        if action == "scale_api":
            if state.get("cost_ratio", 1.0) <= state.get("cost_ceiling", 1.0):
                self.scale.scale_cluster(state.get("region", "default"), state.get("target_replicas", 4))
            else:
                result = {"action": "hold", "reason": "cost_ceiling_exceeded"}

        elif action == "shift_traffic":
            self.scale.shift_traffic(state.get("from_region", "A"), state.get("to_region", "B"), state.get("shift_pct", 20))

        elif action == "rewrite_policy":
            if self._gates_passed(state):
                policy = self.rewrite.propose_patch(
                    state.get("policy_path", "v1/devops/policies/policy_v1.yaml"),
                    state.get("policy_updates", {"latency_threshold": 180}),
                )
                result["policy"] = policy
            else:
                result = {"action": "hold", "reason": "gate_failed"}

        return result
