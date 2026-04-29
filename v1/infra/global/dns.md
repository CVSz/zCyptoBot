# Global DNS Strategy

Use Cloudflare Load Balancer with Geo/Latency steering.

## Records
- `api.zeaz.com` -> pool-region-a (TH priority)
- `api.zeaz.com` -> pool-region-b (SG priority)

## Rules
1. If both pools healthy: route by lowest RTT.
2. If one pool unhealthy: automatic failover to healthy pool.
3. Optional session affinity for sticky execution clients.
