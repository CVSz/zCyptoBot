# V5-V7 Upgrade Blueprint

## v5: RL AI model
- Added `RLV5Policy` and `RLState` to provide a deterministic RL-style policy scaffold.
- Exposes `score()` and discrete `action()` (BUY/SELL/HOLD) for easy drop-in replacement with trained weights.

## v6: Multi-exchange arbitrage
- Added `ArbitrageRouterV6` that composes existing arbitrage detection with balance-aware sizing.
- Produces `ArbitrageExecutionPlan` with venues, size, and expected edge.

## v7: Full K8s + Terraform infra
- Added `InfraBlueprintV7` + `V7InfraConfig` to materialize infrastructure inputs.
- Generates Terraform variable map and Helm values map for environment-specific rollout.
