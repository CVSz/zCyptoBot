# TSS Signing Service

This service defines the isolated threshold-signing boundary for the unified platform.

## Production contract

- API, wallet, trading, and payment services never hold private keys or key shares.
- The coordinator is stateless and accepts only digest-signing requests with tenant, key, trace, and idempotency metadata.
- Signer nodes are isolated workloads with SPIFFE IDs and mTLS-only communication.
- Real signing backends must be wired through `TSS_PROVIDER=frost` or `TSS_PROVIDER=tss-lib` and should store shares wrapped by HSM/KMS/PKCS#11 where available.
- The default backend is intentionally disabled so accidental single-node or mock signing cannot reach production.

## Endpoints

- `GET /healthz`: readiness check with configured provider.
- `POST /v1/sign`: validates request metadata, delegates to the configured threshold backend, and emits an audit event.

## Required environment

| Variable | Default | Purpose |
|---|---|---|
| `TSS_ADDRESS` | `:8088` | HTTP listen address. |
| `ZEAZ_ENV` | `dev` | Environment label. |
| `TSS_PROVIDER` | `disabled` | Must be `frost` or `tss-lib` in production. |
| `TSS_THRESHOLD` | `2` | Required signer threshold. |
| `TSS_PARTICIPANTS` | `3` | Total signer participants. |
| `AUDIT_ENDPOINT` | in-cluster audit URL | Audit sink for every signing decision. |
| `SPIFFE_REQUIRED` | `true` | Documents mandatory workload identity policy. |
