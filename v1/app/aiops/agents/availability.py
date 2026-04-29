from app.aiops.negotiation import Proposal


class AvailabilityAgent:
    def propose(self, state: dict):
        error_rate = state.get("error_rate", 0.0)
        if error_rate >= 0.05:
            return Proposal(
                action="rewrite_policy",
                score=0.8,
                constraints={
                    "ips_dr_pass": state.get("ips_dr_pass", False),
                    "shadow_pass": state.get("shadow_pass", False),
                    "quorum": state.get("quorum_ok", False),
                    "canary_ready": state.get("canary_ready", False),
                    "kill_switch_off": not state.get("kill_switch", False),
                },
            )
        return None
