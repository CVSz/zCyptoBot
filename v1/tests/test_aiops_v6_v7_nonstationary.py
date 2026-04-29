import numpy as np

from app.aiops.bandit_hierarchical import HierarchicalTS
from app.aiops.bandit_ts_ns import LinTS_NS
from app.aiops.counterfactual import doubly_robust, ips
from app.aiops.drift import DriftMonitor
from app.aiops.policy import Policy, PolicyRegistry


def test_lints_ns_discounted_update_changes_state():
    model = LinTS_NS(d=2, discount=0.9)
    x = np.array([[1.0], [0.0]])
    before = model.A["scale_api"].copy()
    model.update("scale_api", x, 1.0)
    assert model.A["scale_api"][0, 0] > before[0, 0]


def test_hierarchical_ts_select_and_update():
    model = HierarchicalTS(d=2)
    x = np.array([[0.5], [0.2]])
    action = model.select("tenant-1", x)
    model.update("tenant-1", action, x, 0.7)
    assert action in model.global_model.A


def test_counterfactual_estimators_return_float():
    logs_ips = [(0.4, 0.5, 1.0), (0.2, 0.4, 0.5)]
    logs_dr = [([1, 0], "scale_api", 0.4, 0.5, 1.0)]
    assert isinstance(ips(logs_ips), float)
    assert isinstance(doubly_robust(logs_dr, lambda _x, _a: 0.2), float)


def test_policy_registry_roundtrip_and_drift_monitor():
    reg = PolicyRegistry()
    p = Policy(id="aiops", version="v7", params={"discount": 0.98})
    reg.register(p)
    assert reg.get("aiops", "v7").params["discount"] == 0.98

    monitor = DriftMonitor(threshold=0.1)
    recent = [1.0] * 40
    baseline = [0.0] * 40
    drifted, stat = monitor.drifted(recent, baseline)
    assert drifted is True
    assert stat > 0
