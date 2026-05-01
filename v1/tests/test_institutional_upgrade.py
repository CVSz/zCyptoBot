from zypto.core.arbitrage import MultiExchangeArbitrage, VenueQuote
from zypto.core.orderbook import OrderbookDepthModel
from zypto.core.rl_cluster import RLClusterConfig, RLTrainingPlanner


def test_orderbook_depth_model_features() -> None:
    model = OrderbookDepthModel()
    bids = [(100.0, 2.0), (99.5, 3.0)]
    asks = [(100.5, 1.0), (101.0, 2.0)]
    snap = model.snapshot(bids, asks, topn=2)
    assert round(model.spread_bps(snap), 2) == 49.88
    assert model.imbalance(snap) > 0


def test_multi_exchange_arbitrage_detects_net_edge() -> None:
    arb = MultiExchangeArbitrage()
    opp = arb.find(
        [
            VenueQuote("binance", bid=100.2, ask=100.3, taker_fee_bps=2.5),
            VenueQuote("okx", bid=100.6, ask=100.7, taker_fee_bps=2.0),
        ],
        min_net_bps=2.0,
    )
    assert opp is not None
    assert opp.buy_venue == "binance"
    assert opp.sell_venue == "okx"


def test_rl_training_planner_resources() -> None:
    planner = RLTrainingPlanner()
    resources = planner.resources(RLClusterConfig(learner_replicas=3, actor_replicas=24, replay_buffer_shards=6, gpu_per_learner=2))
    assert resources["total_gpus"] == 6
    assert resources["actor_pods"] == 24
