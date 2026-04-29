from datetime import datetime

try:
    from clickhouse_driver import Client
except Exception:  # pragma: no cover
    Client = None


class OfflineStore:
    def __init__(self):
        self.db = Client(host="clickhouse") if Client else None

    def write(self, tenant: str, feats: dict, ts: datetime | None = None):
        if not self.db:
            return
        when = ts or datetime.utcnow()
        self.db.execute(
            "INSERT INTO features_offline VALUES",
            [
                (
                    tenant,
                    float(feats["lat"]),
                    float(feats["err"]),
                    float(feats["lag"]),
                    float(feats["hour"]),
                    float(feats["budget"]),
                    float(feats["tier"]),
                    float(feats["traffic"]),
                    when,
                )
            ],
        )
