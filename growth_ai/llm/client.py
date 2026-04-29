from __future__ import annotations

from typing import Any


def generate(prompt: str, context: dict[str, Any]) -> str:
    segment = context.get("segment", "all")
    return f"[GEN]{prompt} :: {segment}"
