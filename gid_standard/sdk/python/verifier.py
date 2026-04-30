import base64
import json
import time
from typing import Dict, Any, Set


class Verifier:
    def __init__(self, trusted_issuers: Set[str], revoked_jti: Set[str] | None = None):
        self.trusted = trusted_issuers
        self.revoked_jti = revoked_jti or set()

    @staticmethod
    def _decode(token: str) -> Dict[str, Any]:
        pad = "=" * (-len(token) % 4)
        return json.loads(base64.urlsafe_b64decode(token + pad))

    def verify(self, token: str) -> Dict[str, Any]:
        data = self._decode(token)

        if data["iss"] not in self.trusted:
            raise ValueError("untrusted issuer")

        if time.time() > data["exp"]:
            raise ValueError("expired")

        if "att" not in data or not data["att"]:
            raise ValueError("missing attestation")

        if data.get("jti") in self.revoked_jti:
            raise ValueError("revoked")

        return data
