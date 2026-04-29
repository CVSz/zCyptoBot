from zcyptobot.v4.governance import ApprovalPolicy, ChangeRequest
from zcyptobot.v4.portfolio import PortfolioAllocator, StrategySlice
from zcyptobot.v4.surveillance import MarketSurveillance


def test_approval_policy_threshold() -> None:
    policy = ApprovalPolicy(max_auto_risk_tier="low")
    assert policy.requires_human_approval(ChangeRequest("risk", "medium", "param tune"))
    assert not policy.requires_human_approval(ChangeRequest("metrics", "low", "dashboard update"))


def test_portfolio_allocator_respects_gross_limit() -> None:
    allocator = PortfolioAllocator()
    weights = allocator.allocate(
        [
            StrategySlice("market_making", target_weight=0.5, expected_vol=0.20),
            StrategySlice("arb", target_weight=0.5, expected_vol=0.10),
        ],
        gross_limit=1.0,
    )
    assert abs(sum(weights.values()) - 1.0) < 1e-9
    assert weights["arb"] > weights["market_making"]


def test_surveillance_detects_quote_instability() -> None:
    surveillance = MarketSurveillance()
    alerts = surveillance.detect_quote_instability(add_rate=12.0, cancel_rate=11.0)
    assert alerts
    assert alerts[0].rule == "QUOTE_INSTABILITY_001"
