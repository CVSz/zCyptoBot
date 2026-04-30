# GID Transport Binding

## mTLS Binding
GID verification is designed to run alongside service mesh mTLS. Implementations should bind the token to the active TLS channel using a channel-binding strategy (for example TLS exporter value in `cnf`).

## Federation and Discovery
- OIDC discovery SHOULD be used for issuer metadata and JWKS retrieval.
- Trust registry MUST map accepted issuers to tenant and regional policy boundaries.

## Replay Mitigation
- Enforce `jti` uniqueness for the token validity window.
- Reject tokens with mismatched channel binding fingerprints.
- Prefer very short TTL (<=10 minutes).
