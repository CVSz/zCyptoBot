# Zypto Documentation Index

This index is a practical map of the repository documentation and where each document is most useful.

## 1) Core Orientation
- [`../README.md`](../README.md): monorepo mission, navigation, and quick start.
- [`DEEP_REPO_OVERVIEW.md`](DEEP_REPO_OVERVIEW.md): deep structural walkthrough and subsystem mapping.
- [`FINAL_RELEASE_DOCUMENTATION.md`](FINAL_RELEASE_DOCUMENTATION.md): consolidated release-facing documentation.

## 2) Product and Platform Docs
- [`product.md`](product.md): product framing and feature narrative.
- [`architecture.md`](architecture.md): technical architecture and core platform concepts.
- [`world_scale_ai_control_system.md`](world_scale_ai_control_system.md): global-scale control-plane perspective.
- [`metrics.md`](metrics.md): KPI/measurement references.

## 3) Business and Growth Docs
- [`business.md`](business.md): business model and market approach.
- [`growth.md`](growth.md): growth engine assumptions and experiments.
- [`financials.md`](financials.md): financial model context.
- [`pitch_deck.md`](pitch_deck.md): pitch narrative structure.

## 4) Prompting and Safety
- [`master-prompts.md`](master-prompts.md): canonical prompt assets.
- [`SAFE_PROJECT_GUIDELINES.md`](SAFE_PROJECT_GUIDELINES.md): safety and operational guardrails.

## 5) Major Codebase Documentation Outside `docs/`
- `v1/README.md`: primary implementation track.
- `v1/docs/*`: versioned architecture and upgrade notes.
- `pitchdeck/README.md`: investor/pitch artifacts.
- `grafana/README.md`: dashboard and observability usage.
- `v1/infra/hft/README.md`: low-latency infra specialization.

## 6) Suggested Reading by Role

### Engineering Lead
1. `../README.md`
2. `DEEP_REPO_OVERVIEW.md`
3. `architecture.md`
4. `v1/README.md`

### Platform/DevOps
1. `architecture.md`
2. `world_scale_ai_control_system.md`
3. `v1/infra/*`
4. `helm/*`, `k8s/*`, `monitoring/*`

### Product/GTM
1. `product.md`
2. `business.md`
3. `growth.md`
4. `pitch_deck.md`
5. `dataroom/*`

### Governance/Compliance
1. `SAFE_PROJECT_GUIDELINES.md`
2. `policy/*`
3. `public_sector_eu/*`
4. `sovereign*/` and `trust_fabric/`

## 7) Maintenance Standard
When adding a major subsystem:
- Update `../README.md` (high-level mention).
- Update `DEEP_REPO_OVERVIEW.md` (detailed placement).
- Add/refresh any domain-specific docs.
- Add links in this index.
