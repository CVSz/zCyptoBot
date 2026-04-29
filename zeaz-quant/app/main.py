import asyncio

from app.config import settings
from app.data.collector import DataCollector
from app.execution.engine import ExecutionEngine
from app.features.builder import FeatureBuilder
from app.risk.manager import RiskManager
from app.signal.engine import SignalEngine
from app.storage.db import Storage

collector = DataCollector()
features = FeatureBuilder()
signal_engine = SignalEngine()
risk = RiskManager(settings.MAX_RISK, settings.MAX_POSITION)
exec_engine = ExecutionEngine()
storage = Storage()

prices: list[float] = []


async def loop() -> None:
    while True:
        data = await collector.get_market()

        prices.append(data["price"])
        if len(prices) < 10:
            await asyncio.sleep(2)
            continue

        feature_set = features.build(prices[-10:], data["oi"], data["sentiment"])
        signal = signal_engine.generate(feature_set)

        if signal == "HOLD":
            await asyncio.sleep(2)
            continue

        size = risk.validate(signal, data["price"])
        if size == 0:
            await asyncio.sleep(2)
            continue

        await exec_engine.execute(signal, size)
        risk.update(signal, size)
        storage.save(signal, size)

        await asyncio.sleep(2)


if __name__ == "__main__":
    asyncio.run(loop())
