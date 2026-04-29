import requests

PROM = "http://prometheus:9090/api/v1/query"


def query(q: str) -> dict:
    return requests.get(PROM, params={"query": q}, timeout=10).json()


def latency_p95() -> dict:
    return query("histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))")


def error_rate() -> dict:
    return query('sum(rate(http_requests_total{status=~"5.."}[5m]))')
