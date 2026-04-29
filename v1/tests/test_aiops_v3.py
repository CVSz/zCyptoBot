from app.aiops.bayesian_rca import BayesianRCA
from app.aiops.rl_planner import RLPlanner


def test_bayesian_rca_returns_ranked_probabilities():
    rca = BayesianRCA()
    ranked = rca.infer({"latency_high": True, "error_high": False, "lag_high": True})

    assert ranked
    assert ranked[0][1] >= ranked[-1][1]
    assert abs(sum(prob for _, prob in ranked) - 1.0) < 1e-6


def test_rl_planner_updates_q_value():
    planner = RLPlanner(alpha=0.5, gamma=0.0, eps=0.0)
    action = planner.select(slo_ok=False, high_lag=True)
    planner.update(False, True, action, reward=2.0, next_slo_ok=True, next_high_lag=False)

    assert planner.Q["0:1"][action] == 1.0
