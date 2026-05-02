# Billing pricing module

`pricing.py` contains static rates and a `price(...)` helper used to compute invoice totals from usage records.

## Behavior

- Supported metrics: `cpu`, `gpu`, `request`.
- Unknown metrics raise `ValueError`.

## Policy / compliance rationale

Rejecting unknown metrics prevents silent under-billing and creates explicit failure signals for downstream audit and finance reconciliation workflows.
