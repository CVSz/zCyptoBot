from prometheus_client import Counter, Histogram, start_http_server

REQ = Counter("api_requests_total", "requests", ["tenant"])
LAT = Histogram("api_latency_seconds", "latency", ["tenant"])


def init_metrics(port: int = 9100):
    start_http_server(port)


def observe(tenant: str, seconds: float):
    REQ.labels(tenant=tenant).inc()
    LAT.labels(tenant=tenant).observe(seconds)
