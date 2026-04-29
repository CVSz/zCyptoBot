EVENTS: list[dict[str, str]] = []


def track(user: str, event: str) -> None:
    EVENTS.append({"user": user, "event": event})
