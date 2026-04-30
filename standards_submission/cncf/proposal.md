# CNCF Proposal: GID + SPIFFE + Istio

- SPIFFE for workload identity
- Istio for mTLS and policy enforcement
- GID as cross-domain identity layer

Reference flow: App -> Envoy -> verify GID -> SPIFFE attestation -> allow/deny
