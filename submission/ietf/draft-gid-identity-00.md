# draft-gid-identity-00

## Status
This Internet-Draft is submitted to IETF for discussion.

## Abstract
GID defines a portable identity token bound to transport (mTLS) and attestation, enabling cross-domain authentication and policy enforcement.

## Requirements
- Tokens MUST expire ≤ 10 minutes
- Tokens MUST include attestation hash
- Implementations MUST verify issuer trust (JWKS)
- Implementations MUST enforce policy (e.g., data residency)

## Security Considerations
- Replay protection (jti + channel binding)
- Key rotation (JWKS, kid)
- Revocation (short TTL + deny list)

## IANA Considerations
- Register "gid" token type
