# Reference Architecture

1. Client presents GID token.
2. Envoy filter validates issuer, TTL, attestation binding, and revocation.
3. SPIFFE identity is checked for workload trust.
4. Regional and data-residency policies are evaluated.
5. Decision is logged for audit.
