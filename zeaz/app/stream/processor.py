import json
import time

from aiokafka import AIOKafkaConsumer

from app.config import settings
from app.execution.engine import ExecutionEngine
from app.risk.engine import RiskEngine
from app.signal.engine import SignalEngine
from app.storage.clickhouse import ClickHouse
from app.observability.metrics import loop_latency, signals_emitted


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
            started = time.perf_counter()
            data = json.loads(msg.value)
            price = data["price"]

            prices.append(price)
            if len(prices) < 10:
                continue

            sig = signal.generate(prices[-10:])
            if sig == "HOLD":
                loop_latency.observe(time.perf_counter() - started)
                continue
            signals_emitted.labels(side=sig).inc()

            size = risk.validate(sig)
            if size == 0:
                continue

            await exec_engine.execute(sig, size)
            risk.update(sig, size)
            db.insert(sig, size, price)
            loop_latency.observe(time.perf_counter() - started)
    finally:
        await consumer.stop()
