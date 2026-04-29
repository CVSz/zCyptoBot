from app.aiops.features import SlidingStats


class Detector:
    def __init__(self):
        self.lat = SlidingStats(120)
        self.err = SlidingStats(120)
        self.lag = SlidingStats(120)

    def ingest(self, metric: dict):
        self.lat.add(metric.get("latency", 0.0))
        self.err.add(metric.get("error_rate", 0.0))
        self.lag.add(metric.get("kafka_lag", 0.0))

    def anomalies(self):
        out = []
        for name, stats, sigma in [
            ("latency", self.lat, 3.0),
            ("error_rate", self.err, 3.0),
            ("kafka_lag", self.lag, 3.0),
        ]:
            mean, std = stats.mean_std()
            if std == 0 or not stats.buf:
                continue
            latest = stats.buf[-1][1]
            z_score = (latest - mean) / std
            if z_score > sigma:
                out.append(
                    {
                        "metric": name,
                        "z": z_score,
                        "value": latest,
                        "mean": mean,
                        "std": std,
                    }
                )
        return out
