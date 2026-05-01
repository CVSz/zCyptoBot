# zypto V4 — Institutional Trading Stack Blueprint

This repository now includes a V4 layer (`src/zypto/v4`) designed as an institutional trading stack foundation, not only a retail bot.

## Stack domains

1. **Research & Signal**: existing `signal`, `core`, and RL modules.
2. **Execution & Smart Routing**: existing execution connectors + cross-venue arbitrage.
3. **Portfolio Construction**: new `PortfolioAllocator` for risk-budgeted capital assignment.
4. **Governance**: new `ApprovalPolicy` for risk-tiered change controls (4-eye principle).
5. **Market Surveillance / Compliance**: new surveillance hooks for abusive pattern detection.
6. **Infra & Deploy**: existing Docker, Helm, Terraform, ArgoCD assets.

## File-by-file additions

- `src/zypto/v4/governance.py`: change-request policy checks.
- `src/zypto/v4/portfolio.py`: inverse-volatility weighted strategy allocation.
- `src/zypto/v4/surveillance.py`: surveillance alerts for quote-instability patterns.
- `src/zypto/v4/__init__.py`: package exports.
- `tests/test_v4_stack.py`: unit tests for new institutional modules.

## Operating model (production-style)

- **Separation of duties**: strategy code changes above low risk require human approval.
- **Capital controls**: portfolio slices normalized to a strict gross exposure cap.
- **Behavioral monitoring**: alerts generated for dangerous quote churn patterns.
- **Progressive hardening**: these modules are deterministic and testable, enabling expansion into full OMS/EMS workflows.
