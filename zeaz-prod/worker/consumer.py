import json
import os

from kafka import KafkaConsumer

consumer = KafkaConsumer(
    "decisions",
    bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP", "localhost:9092"),
    value_deserializer=lambda m: json.loads(m.decode()),
)

for msg in consumer:
    print("PROCESS:", msg.value)
