"""Idempotency utilities for active-active execution safety."""

from __future__ import annotations

import hashlib


def make_key(tenant: str, signal: str, ts: str) -> str:
    """Generate deterministic idempotency key for an execution intent."""
    raw = f"{tenant}:{signal}:{ts}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()
