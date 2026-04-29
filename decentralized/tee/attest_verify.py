import base64
import hashlib


def verify_quote(quote_b64: str, expected_mrenclave: str) -> bool:
    """
    Skeleton verifier:
    - Decode quote
    - Check measurement hash matches expected
    Replace with DCAP/SGX/SEV-SNP library in production.
    """
    raw = base64.b64decode(quote_b64)
    h = hashlib.sha256(raw).hexdigest()
    return h.startswith(expected_mrenclave[:8])
