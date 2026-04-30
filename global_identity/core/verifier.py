import base64
import json
import time

from global_identity.registry.attestations import get as get_att
from global_identity.registry.issuers import is_trusted


def _b64d(x: str) -> dict:
    pad = "=" * (-len(x) % 4)
    return json.loads(base64.urlsafe_b64decode(x + pad))


def verify(token: str, expected_issuer: str):
    data = _b64d(token)
    if data.get("iss") != expected_issuer or not is_trusted(expected_issuer):
        raise ValueError("untrusted issuer")
    if int(time.time()) > int(data.get("exp", 0)):
        raise ValueError("expired")

    att = get_att(data.get("sub"))
    if not att:
        raise ValueError("missing attestation")

    return data
