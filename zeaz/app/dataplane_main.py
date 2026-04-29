import asyncio

from app.ingestion.market import run as ingest


if __name__ == "__main__":
    asyncio.run(ingest())
