# Security Considerations

- MUST use ES256 or EdDSA.
- MUST support key rotation through JWKS.
- MUST bind token to TLS session (exporter-based binding).
- SHOULD verify attestation evidence (TEE/VM identity).
