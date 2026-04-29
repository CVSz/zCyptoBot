from prometheus_client import Counter, Gauge, Histogram, start_http_server

ticks_ingested = Counter("zeaz_ticks_ingested_total", "Total market ticks ingested")
signals_emitted = Counter("zeaz_signals_emitted_total", "Total trading signals emitted", ["side"])
orders_executed = Counter("zeaz_orders_executed_total", "Total execution calls", ["side"])
risk_rejections = Counter("zeaz_risk_rejections_total", "Total orders rejected by risk")
last_price = Gauge("zeaz_last_price", "Latest observed BTCUSDT price")
position = Gauge("zeaz_position", "Current synthetic position")
loop_latency = Histogram("zeaz_stream_loop_seconds", "Stream loop latency in seconds")


def start_metrics_server(port: int = 9000) -> None:
    start_http_server(port)
