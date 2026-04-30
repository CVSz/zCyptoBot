# GID Claims Profile

## Identity Claims
- `sub`: subject identifier
- `iss`: issuer identifier
- `aud`: intended audience

## Tenant and Geography Claims
- `tenant`: logical tenant boundary
- `region`: residency boundary used by policy engine

## Security Claims
- `att`: workload attestation hash / evidence reference
- `jti`: nonce for anti-replay and revocation
- `iat`: issued-at time
- `exp`: expiration time (strictly short-lived)

## Optional Extension Claims
- `scp`: scope list
- `cnf`: confirmation/channel-binding details
- `risk`: dynamic risk score
