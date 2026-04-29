from app.aiops.negotiation import Proposal


class LatencyAgent:
    def propose(self, state: dict):
        latency_ms = state.get("latency", 0)
        threshold = state.get("latency_threshold", 200)
        if latency_ms > threshold:
            return Proposal(
                action="scale_api",
                score=min(1.0, latency_ms / max(threshold, 1)),
                constraints={
                    "safe": state.get("safe_mode", True),
                    "kill_switch_off": not state.get("kill_switch", False),
                },
            )
        return None
