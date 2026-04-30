# Regional Failover

Trigger:
- error_rate > 5% OR latency > 300ms (p95)

Actions:
1. Update global routing → secondary EU region
2. Scale replicas (HPA/KEDA)
3. Validate health checks
4. Notify stakeholders

Target:
- RTO < 30 min
- RPO < 5 min
