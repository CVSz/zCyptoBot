# Global Routing and Failover

## Health endpoints
- `GET /health`
- `GET /ready`

## Failover logic
- Region A down -> route all traffic to Region B.
- Region B down -> route all traffic to Region A.
- Both healthy -> latency-based routing.

## Deploy order
1. Apply region manifests.
2. Apply replication manifests.
3. Enable Cloudflare LB and health checks.
