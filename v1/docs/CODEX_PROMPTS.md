# Codex Prompt Pack (Safe Institutional Variant)

This document provides reusable prompts for generating and extending **zCyptoBot** while explicitly avoiding gambling-style logic.

## Safety and Scope Constraints

Use these constraints in every generation run:

- No gambling-like strategy logic.
- No martingale, doubling down, or all-in behavior.
- Mandatory risk controls (max risk per trade, exposure caps, kill-switches).
- Handle API failures with retries, timeout handling, and idempotency.

## Master Prompt (Institutional Stack)

```text
PROJECT: zcyptobot (AI Quant Trading System)

GOAL:
Build a production-grade crypto trading system using AI + rule-based hybrid strategy.
System must be scalable, secure, and fully automated.

ARCHITECTURE:
- Microservices (FastAPI + Async Python)
- PostgreSQL (TimescaleDB extension)
- Redis (cache + pub/sub)
- Kafka (event streaming)
- Docker + Kubernetes (Helm ready)
- CI/CD (GitHub Actions)

CORE MODULES:
1. DATA INGESTION
2. SIGNAL ENGINE
3. RISK ENGINE (STRICT)
4. EXECUTION ENGINE
5. PORTFOLIO MANAGER
6. BACKTEST ENGINE
7. API LAYER
8. OBSERVABILITY
9. SECURITY

STRATEGY (SAFE HIGH-PERFORMANCE):
- High-volatility asset focus
- OI + momentum + volatility breakout confirmation
- ATR stop-loss and staged take-profit exits
- Explicitly avoid over-leverage, martingale, and all-in behavior

CONSTRAINTS:
- NO gambling-like logic
- NO martingale / doubling down
- MUST include risk management
- MUST handle API errors, timeouts, retries

OUTPUT:
- Full project structure
- Docker + docker-compose
- Helm chart
- CI pipeline
- README with setup steps
```

## Advanced Extension Prompt

```text
EXTENSION:
- Add reinforcement learning module (optional)
- Add feature store (Feast)
- Add vector DB (pgvector) for sentiment embedding
- Add anomaly detection (flash crash protection)
- Add multi-agent components:
  - Scout agent (data)
  - Analyst agent (signal)
  - Executor agent (trade)
```

## Practical Prompting Tips

- Start with the master prompt and generate a minimal vertical slice first.
- Ask for strict typing and async-first implementation details.
- Require deterministic tests for risk and execution behavior.
- Add non-functional requirements (observability, security, and deployment) before scaling module count.
