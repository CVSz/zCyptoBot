from app.aiops.negotiation import Proposal


class RegionAgent:
    def propose(self, state: dict):
        region_load = state.get("region_load", 0.0)
        if region_load > 0.8:
            return Proposal(
                action="shift_traffic",
                score=0.9,
                constraints={
                    "multi_region": state.get("multi_region", False),
                    "safe": state.get("safe_mode", True),
                    "kill_switch_off": not state.get("kill_switch", False),
                },
            )
        return None
