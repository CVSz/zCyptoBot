"""Basic anti-sybil identity fingerprint checks."""

import hashlib

IDENTITY = {}


def register(node_id: str, fingerprint: str) -> None:
    h = hashlib.sha256(fingerprint.encode()).hexdigest()
    if h in IDENTITY.values():
        raise ValueError("sybil detected")
    IDENTITY[node_id] = h
