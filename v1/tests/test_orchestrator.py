from zcyptobot import BotConfig, Orchestrator


def test_orchestrator_cycle_produces_stats():
    orchestrator = Orchestrator(BotConfig(symbols=("BTCUSDT", "ETHUSDT", "SOLUSDT")))
    stats = orchestrator.run_cycle()
    assert stats.ticks > 0
    assert 0 <= stats.accepted <= stats.ticks
    assert stats.equity > 0


def test_orchestrator_can_run_multiple_cycles():
    orchestrator = Orchestrator(BotConfig(symbols=("BTCUSDT", "ETHUSDT")))
    equities = [orchestrator.run_cycle().equity for _ in range(20)]
    assert all(eq > 0 for eq in equities)
