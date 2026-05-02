import json
import os

from kafka import KafkaProducer


def _serialize(payload: dict) -> bytes:
    return json.dumps(payload).encode()


producer = KafkaProducer(
    bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP", "localhost:9092"),
    value_serializer=_serialize,
)


def publish(topic: str, data: dict) -> None:
    producer.send(topic, data)
    producer.flush()
