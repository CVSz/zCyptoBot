"""Mutable policy store with apply helper."""

POLICY = {"latency_limit": 200}


def apply(change) -> None:
    POLICY.update(change)
