import orjson
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer


class KafkaBus:
    def __init__(self, brokers: str = "kafka:9092"):
        self.brokers = brokers
        self.producer = AIOKafkaProducer(bootstrap_servers=self.brokers)

    async def start(self):
        await self.producer.start()

    async def publish(self, topic: str, data: dict):
        await self.producer.send_and_wait(topic, orjson.dumps(data))

    async def stop(self):
        await self.producer.stop()


class KafkaConsumerWrapper:
    def __init__(self, topic: str, brokers: str = "kafka:9092"):
        self.consumer = AIOKafkaConsumer(
            topic,
            bootstrap_servers=brokers,
            value_deserializer=lambda m: orjson.loads(m),
        )

    async def start(self):
        await self.consumer.start()

    async def listen(self):
        async for msg in self.consumer:
            yield msg.value
