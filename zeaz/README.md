# ZEAZ SCANNET + Automos Meta V3

Production baseline for a local quant stack (Ryzen 5 3400G / 32GB RAM / NVMe) with separated data-plane and control-plane services.

## Architecture

`Ingestion -> Kafka -> Stream Processor -> ClickHouse`

- **Dataplane**: `app/dataplane_main.py` (market ingestion only)
- **Control plane**: `app/control_main.py` (signal + risk + execution + persistence)
- **Observability**: Prometheus metrics on `:9000/metrics`

## Run

```bash
cd zeaz/infra
docker compose up --build
```

## Key Metrics

- `zeaz_ticks_ingested_total`
- `zeaz_signals_emitted_total{side}`
- `zeaz_orders_executed_total{side}`
- `zeaz_risk_rejections_total`
- `zeaz_last_price`
- `zeaz_position`
- `zeaz_stream_loop_seconds`


## Observability Dashboard

- Prometheus: `http://localhost:9090`
- Grafana: `http://localhost:3000` (default `admin/admin`)
- Prometheus datasource is auto-provisioned.
