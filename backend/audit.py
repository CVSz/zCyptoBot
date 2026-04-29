import time
from typing import Any

LOGS: list[dict[str, Any]] = []


def log_event(user: str, action: str, resource: str) -> None:
    LOGS.append(
        {
            "user": user,
            "action": action,
            "resource": resource,
            "ts": time.time(),
        }
    )


def query_logs(user: str | None = None) -> list[dict[str, Any]]:
    return [entry for entry in LOGS if user is None or entry["user"] == user]
