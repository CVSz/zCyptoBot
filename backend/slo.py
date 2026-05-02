import os
from typing import Any, Dict
from requests import Session, RequestException

# Read Prometheus endpoint from environment to avoid hard-coded endpoints.
PROMETHEUS_ENDPOINT = os.getenv("PROMETHEUS_ENDPOINT", "http://prometheus:9090")
PROM_QUERY_URL = f"{PROMETHEUS_ENDPOINT.rstrip('/')}/api/v1/query"

_session = Session()
_session.headers.update({"Accept": "application/json"})


def query(q: str, timeout: int = 10) -> Dict[str, Any]:
    try:
        resp = _session.get(PROM_QUERY_URL, params={"query": q}, timeout=timeout)
        resp.raise_for_status()
        return resp.json()
    except RequestException:
        # Let the caller handle the exception; surface useful context if needed.
        raise


def latency_p95() -> Dict[str, Any]:
    return query("histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))")


def error_rate() -> Dict[str, Any]:
    return query('sum(rate(http_requests_total{status=~"5.."}[5m]))')
