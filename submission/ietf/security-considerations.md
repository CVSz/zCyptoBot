# Security Considerations

- Replay protection via `jti` and mTLS channel binding.
- Frequent key rotation using JWKS and `kid` pinning.
- Revocation enforced by short-lived tokens plus deny-list checks.
- Tenant isolation and policy-first default deny posture.
