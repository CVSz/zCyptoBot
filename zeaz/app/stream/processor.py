import json

from aiokafka import AIOKafkaConsumer

from app.config import settings
from app.execution.engine import ExecutionEngine
from app.risk.engine import RiskEngine
from app.signal.engine import SignalEngine
from app.storage.clickhouse import ClickHouse


async def run() -> None:
    consumer = AIOKafkaConsumer(
        "market",
        bootstrap_servers=settings.KAFKA_BROKER,
        group_id="zeaz",
        auto_offset_reset="latest",
    )
    await consumer.start()

    signal = SignalEngine()
    risk = RiskEngine(settings.MAX_RISK, settings.MAX_POSITION)
    exec_engine = ExecutionEngine()
    db = ClickHouse()

    prices: list[float] = []

    try:
        async for msg in consumer:
            data = json.loads(msg.value)
            price = data["price"]

            prices.append(price)
            if len(prices) < 10:
                continue

            sig = signal.generate(prices[-10:])
            if sig == "HOLD":
                continue

            size = risk.validate(sig)
            if size == 0:
                continue

            await exec_engine.execute(sig, size)
            risk.update(sig, size)
            db.insert(sig, size, price)
    finally:
        await consumer.stop()
