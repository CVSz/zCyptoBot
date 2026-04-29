from dataclasses import dataclass, field


@dataclass(slots=True)
class RiskConfig:
    max_position_usd: float = 10_000.0
    max_symbol_weight: float = 0.30
    max_gross_exposure_usd: float = 25_000.0
    stop_loss_pct: float = 0.02
    take_profit_pct: float = 0.05
    max_drawdown_pct: float = 0.12
    risk_per_trade_pct: float = 0.01


@dataclass(slots=True)
class SignalConfig:
    lookback: int = 20
    volatility_floor: float = 0.01
    sentiment_threshold: float = 0.60
    oi_accumulation_threshold: float = 0.03


@dataclass(slots=True)
class ExecutionConfig:
    slippage_bps: float = 4.0
    fee_bps: float = 5.0
    min_order_usd: float = 50.0


@dataclass(slots=True)
class BotConfig:
    initial_cash: float = 100_000.0
    symbols: tuple[str, ...] = ("BTCUSDT", "ETHUSDT", "SOLUSDT")
    signal: SignalConfig = field(default_factory=SignalConfig)
    risk: RiskConfig = field(default_factory=RiskConfig)
    execution: ExecutionConfig = field(default_factory=ExecutionConfig)
