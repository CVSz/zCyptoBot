import json
import os

from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP", "localhost:9092"),
    value_serializer=lambda v: json.dumps(v).encode(),
)


def publish(topic: str, data: dict) -> None:
    producer.send(topic, data)
    producer.flush()
