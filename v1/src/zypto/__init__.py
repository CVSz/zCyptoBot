"""Backward-compatible package alias for legacy `zypto` imports."""

from importlib import import_module
import sys

from zcyptobot import *  # noqa: F401,F403

_ALIAS_MODULES = {
    "zypto": "zcyptobot",
    "zypto.config": "zcyptobot.config",
    "zypto.models": "zcyptobot.models",
    "zypto.pipeline": "zcyptobot.pipeline",
    "zypto.simulator": "zcyptobot.simulator",
    "zypto.core": "zcyptobot.core",
    "zypto.core.arbitrage": "zcyptobot.core.arbitrage",
    "zypto.core.orderbook": "zcyptobot.core.orderbook",
    "zypto.core.rl_cluster": "zcyptobot.core.rl_cluster",
    "zypto.core.rl_v5": "zcyptobot.core.rl_v5",
    "zypto.core.arbitrage_v6": "zcyptobot.core.arbitrage_v6",
    "zypto.core.infra_v7": "zcyptobot.core.infra_v7",
    "zypto.risk": "zcyptobot.risk",
    "zypto.risk.engine": "zcyptobot.risk.engine",
    "zypto.signal": "zcyptobot.signal",
    "zypto.signal.engine": "zcyptobot.signal.engine",
    "zypto.v4": "zcyptobot.v4",
    "zypto.v4.governance": "zcyptobot.v4.governance",
    "zypto.v4.portfolio": "zcyptobot.v4.portfolio",
    "zypto.v4.surveillance": "zcyptobot.v4.surveillance",
}

for alias, target in _ALIAS_MODULES.items():
    sys.modules.setdefault(alias, import_module(target))
