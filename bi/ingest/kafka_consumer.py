from __future__ import annotations

import hashlib
import json
import os
from typing import Any

from clickhouse_driver import Client
from confluent_kafka import Consumer

KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "events")
KAFKA_BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP", "kafka:9092")
GROUP_ID = os.getenv("KAFKA_GROUP", "bi")
PII_SALT = os.getenv("PII_SALT", "local-dev-salt")

consumer = Consumer(
    {
        "bootstrap.servers": KAFKA_BOOTSTRAP,
        "group.id": GROUP_ID,
        "auto.offset.reset": "earliest",
        "enable.auto.commit": True,
    }
)
consumer.subscribe([KAFKA_TOPIC])

db = Client(host=os.getenv("CLICKHOUSE_HOST", "clickhouse"))


def _hash_user_id(user_id: str) -> str:
    return hashlib.sha256(f"{PII_SALT}:{user_id}".encode("utf-8")).hexdigest()


def _normalize_event(payload: dict[str, Any]) -> tuple:
    props = payload.get("props", {})
    return (
        payload["ts"],
        _hash_user_id(str(payload["user_id"])),
        str(payload["tenant_id"]),
        str(payload["event"]),
        json.dumps(props),
        int(bool(payload.get("consent", {}).get("email", False))),
        int(bool(payload.get("consent", {}).get("sms", False))),
        int(bool(payload.get("consent", {}).get("push", False))),
    )


def run() -> None:
    while True:
        msg = consumer.poll(1.0)
        if msg is None or msg.error():
            continue

        data = json.loads(msg.value())
        row = _normalize_event(data)
        db.execute("INSERT INTO events VALUES", [row])


if __name__ == "__main__":
    run()
