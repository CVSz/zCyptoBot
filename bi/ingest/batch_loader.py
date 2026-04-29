from __future__ import annotations

import hashlib
import json
import os
from typing import Any

from clickhouse_driver import Client

PII_SALT = os.getenv("PII_SALT", "local-dev-salt")


def _hash_user_id(user_id: str) -> str:
    return hashlib.sha256(f"{PII_SALT}:{user_id}".encode("utf-8")).hexdigest()


def load_file(path: str) -> int:
    db = Client(host=os.getenv("CLICKHOUSE_HOST", "clickhouse"))
    rows: list[tuple[Any, ...]] = []

    with open(path, "r", encoding="utf-8") as handle:
        for line in handle:
            payload = json.loads(line)
            rows.append(
                (
                    payload["ts"],
                    _hash_user_id(str(payload["user_id"])),
                    str(payload["tenant_id"]),
                    str(payload["event"]),
                    json.dumps(payload.get("props", {})),
                    int(bool(payload.get("consent", {}).get("email", False))),
                    int(bool(payload.get("consent", {}).get("sms", False))),
                    int(bool(payload.get("consent", {}).get("push", False))),
                )
            )

    if rows:
        db.execute("INSERT INTO events VALUES", rows)
    return len(rows)


if __name__ == "__main__":
    filepath = os.getenv("BATCH_EVENTS_FILE", "events.jsonl")
    inserted = load_file(filepath)
    print(f"inserted={inserted}")
