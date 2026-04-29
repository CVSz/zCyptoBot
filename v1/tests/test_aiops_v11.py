from app.aiops.negotiation import NegotiationEngine, Proposal
from app.aiops.orchestrator_v11 import AIOpsV11


class StubAgent:
    def __init__(self, proposal=None):
        self._proposal = proposal

    def propose(self, state):
        return self._proposal


def test_negotiation_filters_constraints():
    engine = NegotiationEngine(
        [
            StubAgent(Proposal("scale_api", 1.0, {"safe": False})),
            StubAgent(Proposal("shift_traffic", 0.7, {"safe": True})),
        ]
    )
    assert engine.negotiate({}) == "shift_traffic"


def test_orchestrator_rewrite_requires_gates():
    aiops = AIOpsV11(agents=[StubAgent(Proposal("rewrite_policy", 0.9, {"ok": True}))])
    blocked = aiops.step({"kill_switch": False})
    assert blocked["action"] == "hold"
    assert blocked["reason"] == "gate_failed"


def test_orchestrator_rewrite_when_ready(tmp_path):
    aiops = AIOpsV11(agents=[StubAgent(Proposal("rewrite_policy", 0.9, {"ok": True}))])
    policy_path = tmp_path / "policy.yaml"
    policy_path.write_text("version: v1\nrules:\n  latency_threshold: 200\n", encoding="utf-8")

    result = aiops.step(
        {
            "kill_switch": False,
            "shadow_pass": True,
            "simulator_pass": True,
            "ips_dr_pass": True,
            "quorum_ok": True,
            "canary_ready": True,
            "policy_path": str(policy_path),
            "policy_updates": {"latency_threshold": 180},
        }
    )
    assert result["action"] == "rewrite_policy"
    assert result["policy"]["rules"]["latency_threshold"] == 180
