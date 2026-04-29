import sqlite3


class Storage:
    def __init__(self, db_path: str = "data.db") -> None:
        self.conn = sqlite3.connect(db_path)
        self.conn.execute(
            "CREATE TABLE IF NOT EXISTS trades (signal TEXT, size REAL)"
        )

    def save(self, signal: str, size: float) -> None:
        self.conn.execute("INSERT INTO trades VALUES (?, ?)", (signal, size))
        self.conn.commit()
