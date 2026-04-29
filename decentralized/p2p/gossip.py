SUBSCRIBERS = []


def subscribe(cb):
    SUBSCRIBERS.append(cb)


def publish(topic: str, payload: dict):
    msg = {"topic": topic, "payload": payload}
    for cb in SUBSCRIBERS:
        cb(msg)
