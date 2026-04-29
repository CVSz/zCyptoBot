import asyncio

from app.observability.metrics import start_metrics_server
from app.stream.processor import run as processor


async def main() -> None:
    start_metrics_server()
    await processor()


if __name__ == "__main__":
    asyncio.run(main())
