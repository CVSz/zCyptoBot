from clickhouse_driver import Client

from app.tenancy.context import get_tenant


class ClickHouse:
    def __init__(self, host: str = "clickhouse"):
        self.client = Client(host=host)

    def insert(self, signal, size, price, sentiment=0.0, whale=0.0):
        tenant = get_tenant()
        self.client.execute(
            "INSERT INTO trades VALUES",
            [(tenant, signal, size, price, sentiment, whale)],
        )
