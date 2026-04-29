# ZCYPTOBOT v2

Institutional AI quant crypto trading platform scaffold with async, event-driven components.

## Core services included

- API-ready orchestrator and modular engines
- Kafka event bus wrapper (`EventBus`) + Redis Streams bus (`RedisStreamsBus`)
- Market ingestion stream (`BinanceStream`)
- Multi-factor signal engine (volatility + OI divergence)
- Institutional risk engine (drawdown kill-switch and sizing)
- Multi-exchange execution adapter baseline (`BaseExchange`, `BinanceExchange`)
- Orderbook depth microstructure model + cross-exchange arbitrage detector
- RL training cluster capacity planner + GitOps/IaC scaffolding (ArgoCD + Terraform)
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


## Enterprise upgrade scaffold

- `src/zcyptobot/core/orderbook.py`: top-N depth features (VWAP, imbalance, spread bps)
- `src/zcyptobot/core/arbitrage.py`: multi-exchange net-edge arbitrage evaluator
- `src/zcyptobot/core/streams.py`: Redis Streams producer/consumer group wrapper
- `src/zcyptobot/core/rl_cluster.py`: distributed RL cluster resource planner
- `deploy/argocd/application.yaml`: ArgoCD app-of-apps style deployment entry
- `deploy/terraform/`: Terraform module skeleton for trading infra sizing
