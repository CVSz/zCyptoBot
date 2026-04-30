class Lakehouse:
    """
    Append-only storage + query interface (ClickHouse/Delta-like).
    """

    def __init__(self):
        self.rows = []

    def append(self, row: dict):
        self.rows.append(row)

    def query(self, predicate):
        return [r for r in self.rows if predicate(r)]
