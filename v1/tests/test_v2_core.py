from zcyptobot.risk.engine import RiskEngine
from zcyptobot.signal.engine import SignalEngine


def test_signal_engine_long():
    s = SignalEngine()
    assert s.compute([1, 2, 3, 4], 200, 100) == "LONG"


def test_risk_engine_size_and_drawdown():
    r = RiskEngine(0.02, 0.2, initial_equity=10000)
    assert round(r.size(100), 3) == 2.0
    assert r.check_drawdown() is True
