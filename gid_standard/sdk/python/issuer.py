import base64
import json
import time
import uuid
from typing import Dict, Any


class Issuer:
    def __init__(self, issuer: str, default_ttl_seconds: int = 600):
        if default_ttl_seconds > 600:
            raise ValueError("TTL must be <= 10 minutes")
        self.issuer = issuer
        self.default_ttl_seconds = default_ttl_seconds

    @staticmethod
    def _encode(payload: Dict[str, Any]) -> str:
        raw = json.dumps(payload, separators=(",", ":")).encode()
        return base64.urlsafe_b64encode(raw).decode().rstrip("=")

    def mint(self, subject: str, audience: str, tenant: str, region: str, attestation_hash: str) -> str:
        now = int(time.time())
        payload = {
            "sub": subject,
            "iss": self.issuer,
            "aud": audience,
            "tenant": tenant,
            "region": region,
            "att": attestation_hash,
            "iat": now,
            "exp": now + self.default_ttl_seconds,
            "jti": str(uuid.uuid4()),
        }
        return self._encode(payload)
