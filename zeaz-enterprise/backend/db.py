import os

import psycopg


class TenantConnection:
    def __init__(self, tenant: str):
        self.tenant = tenant
        self.conn = psycopg.connect(os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/postgres"))

    def __enter__(self):
        with self.conn.cursor() as cur:
            cur.execute("SELECT set_config('app.tenant', %s, false)", (self.tenant,))
        return self.conn

    def __exit__(self, exc_type, exc, tb):
        self.conn.close()
