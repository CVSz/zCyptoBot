import os

from psycopg2.pool import SimpleConnectionPool

_pool = SimpleConnectionPool(
    1,
    10,
    os.getenv(
        "DATABASE_URL",
        "dbname=zeaz user=postgres password=postgres host=localhost port=5432",
    ),
)


def init_db() -> None:
    conn = _pool.getconn()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS decisions (
                    id SERIAL PRIMARY KEY,
                    tenant TEXT NOT NULL,
                    action TEXT NOT NULL,
                    reward DOUBLE PRECISION NOT NULL,
                    created_at TIMESTAMPTZ DEFAULT now()
                )
                """
            )
            conn.commit()
    finally:
        _pool.putconn(conn)


def save_decision(tenant: str, action: str, reward: float) -> None:
    conn = _pool.getconn()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO decisions (tenant, action, reward) VALUES (%s,%s,%s)",
                (tenant, action, reward),
            )
            conn.commit()
    finally:
        _pool.putconn(conn)
