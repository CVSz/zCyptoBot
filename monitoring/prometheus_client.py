import requests


def query_prometheus(query: str, endpoint: str = "http://prometheus:9090") -> dict:
    response = requests.get(f"{endpoint}/api/v1/query", params={"query": query}, timeout=10)
    response.raise_for_status()
    return response.json()


def current_kpi_state() -> dict:
    latency = query_prometheus(
        "histogram_quantile(0.95, sum by (le) (rate(http_request_duration_seconds_bucket[5m])))"
    )
    error = query_prometheus(
        'sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total[5m]))'
    )
    return {"latency": latency, "error": error}
