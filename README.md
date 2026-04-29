# ZCYPTOBOT

Institutional-grade AI Quant Trading System template for research and development.

## Overview

ZCYPTOBOT is a modular, event-driven trading platform concept that emphasizes:

- Discipline over prediction
- Risk-first execution
- Automated workflows with strong guardrails

## Implemented Architecture

```text
[Market Data] -> [Data Filter] -> [Signal Engine] -> [Risk Engine] -> [Execution Engine] -> [Portfolio]
```

## Included Components

- `DataFilter`: validates symbols and sanitizes noisy ticks
- `SignalEngine`: sentiment + volatility + open-interest accumulation model
- `RiskEngine`: risk-budget sizing, drawdown kill-switch, exposure caps
- `ExecutionEngine`: slippage/fees aware paper execution
- `Portfolio`: position + cash accounting
- `QuantBot`: orchestration pipeline
- `Simulator`: synthetic market generator for end-to-end testing
- `Orchestrator`: service-level run cycle that coordinates social discovery + market ingestion

## Quick Start

```bash
python -m pip install -e .
pytest
python -c "from zcyptobot.simulator import run_simulation; print(run_simulation())"
python -c "from zcyptobot import Orchestrator; o=Orchestrator(); print(o.run_cycle())"
```

## Disclaimer

This repository is for educational and research purposes only. Trading digital assets involves substantial risk, including total loss of capital. There is no guarantee of profit.

## License

Distributed under the MIT License. See `LICENSE`.
