# GID Standard Specification

## Token Header Requirements
- `alg`: ES256 (**MUST**)
- `kid`: key identifier (**MUST**)

## Required Claims
- `sub`, `iss`, `aud` (**MUST**)
- `tenant`, `region` (**MUST**)
- `att` (attestation hash) (**MUST**)
- `iat`, `exp` with token lifetime `<= 10 minutes` (**MUST**)
- `jti` (nonce) (**MUST**)

## Security Requirements
- Implementations **MUST** support key rotation.
- Implementations **MUST** support revocation (`jti` denylist and/or short TTL).
- Tokens **MUST** be bound to mTLS channel context (channel binding).

## Compliance Requirements
- Implementations **MUST** enforce data residency policy.
- Implementations **MUST** log all authorization decisions.
