from zcyptobot.core.arbitrage import VenueQuote
from zcyptobot.core.arbitrage_v6 import ArbitrageRouterV6, ExchangeBalance
from zcyptobot.core.infra_v7 import InfraBlueprintV7, V7InfraConfig
from zcyptobot.core.rl_v5 import RLV5Policy, RLState


def test_v5_rl_policy_actions() -> None:
    policy = RLV5Policy()
    assert policy.action(RLState(momentum=0.8, volatility=0.1, orderbook_imbalance=0.4)) == "BUY"
    assert policy.action(RLState(momentum=-0.7, volatility=0.2, orderbook_imbalance=-0.3)) == "SELL"


def test_v6_arbitrage_router_builds_plan() -> None:
    router = ArbitrageRouterV6()
    plan = router.plan(
        quotes=[
            VenueQuote("binance", bid=100.1, ask=100.2, taker_fee_bps=2.0),
            VenueQuote("bybit", bid=100.6, ask=100.7, taker_fee_bps=2.0),
        ],
        balances=[
            ExchangeBalance("binance", quote_balance=2_000.0, base_balance=0.0),
            ExchangeBalance("bybit", quote_balance=100.0, base_balance=4.0),
        ],
        min_net_bps=5.0,
    )
    assert plan is not None
    assert plan.buy_venue == "binance"
    assert plan.sell_venue == "bybit"


def test_v7_infra_blueprint_materializes_configs() -> None:
    bp = InfraBlueprintV7()
    cfg = V7InfraConfig(region="us-west-2", rl_learner_replicas=4, rl_actor_replicas=30)
    tf_vars = bp.terraform_vars(cfg)
    helm_values = bp.helm_values(cfg)

    assert tf_vars["region"] == "us-west-2"
    assert tf_vars["rl_node_group_size"] == 9
    assert helm_values["rl"]["learners"] == 4
