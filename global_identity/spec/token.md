# GID Token (JSON, signed)

Header:
- alg (e.g., ES256)
- kid (key id)

Claims:
- sub (subject)
- iss (issuer DID/URL)
- aud (service)
- tenant
- region
- att (attestation hash)
- iat / exp (short TTL, e.g., 5–10 min)
- jti (nonce)
