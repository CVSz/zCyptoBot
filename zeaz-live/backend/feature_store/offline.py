from clickhouse_driver import Client

db = Client(host="localhost")


def insert(tenant: str, f: dict):
    db.execute(
        "INSERT INTO features VALUES",
        [(tenant, f["latency"], f["error"], f["load"])],
    )
