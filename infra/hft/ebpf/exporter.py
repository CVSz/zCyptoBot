import time
from prometheus_client import Gauge, start_http_server

latency = Gauge("order_latency_ns", "Order path latency in nanoseconds")


def main() -> None:
    start_http_server(9100)
    while True:
        latency.set(1000)
        time.sleep(1)


if __name__ == "__main__":
    main()
