from __future__ import annotations

from collections.abc import Iterable

from growth_ai.personalization.engine import message


def run_campaign(users: Iterable[dict]) -> list[dict[str, str]]:
    outputs: list[dict[str, str]] = []
    for user in users:
        msg = message(user)
        outputs.append({"user": str(user["id"]), "msg": msg})
    return outputs
