from collections import deque


class StreamBus:
    """
    Simplified stream bus (Kafka-like semantics).
    """

    def __init__(self):
        self.topics = {}

    def publish(self, topic: str, msg: dict):
        self.topics.setdefault(topic, deque()).append(msg)

    def consume(self, topic: str):
        q = self.topics.get(topic, deque())
        while q:
            yield q.popleft()
