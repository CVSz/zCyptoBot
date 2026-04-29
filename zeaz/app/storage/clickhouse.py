from clickhouse_driver import Client

from app.config import settings


class ClickHouse:
    def __init__(self):
        self.client = Client(host=settings.CLICKHOUSE_HOST)

    def insert(self, signal: str, size: float, price: float) -> None:
        self.client.execute("INSERT INTO trades (signal, size, price) VALUES", [(signal, size, price)])
