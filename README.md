# ZCYPTOBOT v2

Institutional AI quant crypto trading platform scaffold with async, event-driven components.

## Core services included

- API-ready orchestrator and modular engines
- Kafka event bus wrapper (`EventBus`)
- Market ingestion stream (`BinanceStream`)
- Multi-factor signal engine (volatility + OI divergence)
- Institutional risk engine (drawdown kill-switch and sizing)
- Multi-exchange execution adapter baseline (`BaseExchange`, `BinanceExchange`)
- Docker, docker-compose, GitHub Actions CI, and Helm chart scaffold

## Quick start

```bash
python -m pip install -e .
pytest
python -m zcyptobot
```

## Infrastructure

- `docker-compose up --build` for local stack (app + Redis + TimescaleDB + Kafka)
- Helm chart in `deploy/helm/zcyptobot`
- CI workflow in `.github/workflows/build-deploy.yml`

## Disclaimer

Research and education only. No performance guarantees.
