# GID Conformance Rules

A compliant implementation **MUST**:
- reject expired tokens
- reject untrusted issuers
- enforce attestation validation
- enforce policy (PII cross-border deny)
- produce audit logs

## Required Test Vectors
- valid token
- expired token
- tampered token
- revoked token
