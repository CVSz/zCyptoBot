from collections import defaultdict

try:
    from clickhouse_driver import Client
except Exception:  # pragma: no cover - optional dependency in local dev
    Client = None


class LearnedPriors:
    def __init__(self):
        self.db = Client(host="clickhouse") if Client else None
        self.priors = defaultdict(float)
        self.counts = defaultdict(lambda: defaultdict(int))
        self.cause_counts = defaultdict(int)

    def ingest_incident(self, cause: str, evidence: dict):
        self.cause_counts[cause] += 1
        for signal, present in evidence.items():
            if present:
                self.counts[signal][cause] += 1

    def recompute(self, alpha: float = 1.0):
        if not self.cause_counts:
            return {}, {}

        total = sum(self.cause_counts.values()) + alpha * len(self.cause_counts)
        for cause, count in self.cause_counts.items():
            self.priors[cause] = (count + alpha) / total

        likelihoods = {}
        for signal, mapping in self.counts.items():
            likelihoods[signal] = {}
            for cause, c_total in self.cause_counts.items():
                numerator = mapping.get(cause, 0) + alpha
                denominator = c_total + 2 * alpha
                likelihoods[signal][cause] = numerator / denominator

        return dict(self.priors), likelihoods
