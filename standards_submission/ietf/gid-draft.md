# draft-gid-identity-00

## Abstract
Global Identity (GID) defines a portable, verifiable identity token bound to transport (mTLS) and attestation, enabling cross-domain authentication without vendor lock-in.

## Requirements
- Short-lived tokens (<=10 min)
- Mandatory attestation binding
- Channel binding to TLS session
- Issuer federation (trust registry)

## Security
- Replay prevention (`jti` + channel binding)
- Key rotation (`kid` + JWKS)
- Revocation (short TTL + deny lists)
