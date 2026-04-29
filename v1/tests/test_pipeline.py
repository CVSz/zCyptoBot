from zcyptobot.config import BotConfig
from zcyptobot.models import MarketTick
from zcyptobot.pipeline import QuantBot
from zcyptobot.simulator import run_simulation


def test_bot_accepts_valid_ticks_and_updates_equity():
    bot = QuantBot(BotConfig(symbols=("BTCUSDT",)))
    for i in range(50):
        tick = MarketTick(i, "BTCUSDT", 100 + i * 0.2, 1000, 0.8, 1000 + i * 20)
        result = bot.on_tick(tick)
        assert result.accepted
    assert bot.portfolio.market_value(bot.marks) > 0


def test_bot_rejects_invalid_symbol():
    bot = QuantBot(BotConfig(symbols=("BTCUSDT",)))
    tick = MarketTick(1, "DOGEUSDT", 10, 100, 0.5, 1000)
    result = bot.on_tick(tick)
    assert not result.accepted


def test_simulation_runs_end_to_end():
    report = run_simulation(BotConfig(symbols=("BTCUSDT", "ETHUSDT")), ticks_per_symbol=120)
    assert report.final_equity > 0
    assert report.accepted_ticks > 0
