from clickhouse_driver import Client

db = Client(host="localhost")


def insert(data):
    db.execute("INSERT INTO features VALUES", [data])
