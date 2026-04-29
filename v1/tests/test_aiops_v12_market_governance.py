from app.aiops.governance.policy_guard import PolicyGuard
from app.aiops.governance.voting import Voting
from app.aiops.market.clearing import clear_market


def test_double_auction_clears_when_prices_cross():
    bids = [{"agent": "b1", "res": "cpu", "price": 0.8, "qty": 2}]
    asks = [{"agent": "s1", "res": "cpu", "price": 0.4, "qty": 1}]
    trades = clear_market(bids, asks)
    assert len(trades) == 1
    assert trades[0].qty == 1
    assert trades[0].price == 0.6


def test_weighted_vote_threshold():
    voting = Voting(threshold=0.7, min_quorum=2)
    voting.vote("a", True, weight=0.8)
    voting.vote("b", False, weight=0.2)
    assert voting.result() is True


def test_policy_guard_cost_ceiling():
    guard = PolicyGuard(max_cost=1.0)
    assert guard.allow({"type": "scale_cluster", "cost": 0.9}) is True
    assert guard.allow({"type": "scale_cluster", "cost": 1.1}) is False
