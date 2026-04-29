import asyncio

from app.ingestion.market import run as ingest
from app.stream.processor import run as processor


async def main() -> None:
    await asyncio.gather(ingest(), processor())


if __name__ == "__main__":
    asyncio.run(main())
