# Ultra-Low Latency HFT Data Plane Blueprint

This blueprint provides a deployable starting point for Ubuntu 24.04 on-prem environments targeting HFT-grade latency.

## Architecture

```text
[Exchange NIC]
     ↓ (Kernel bypass: DPDK / AF_XDP)
[User-space Feed Handler] ──→ [Strategy Engine]
        ↓                           ↓
   eBPF telemetry              FPGA (optional offload)
        ↓                           ↓
     Prometheus               Order Gateway → NIC
```

## Contents

- `ebpf/latency.c`: BCC-compatible eBPF latency probe for send path tracing.
- `ebpf/exporter.py`: Prometheus exporter skeleton for latency metrics.
- `ebpf/run_probe.py`: Probe loader script.
- `dpdk/rx.c`: Minimal DPDK RX loop skeleton.
- `afxdp/xdp_prog.c`: Minimal XDP program scaffold.
- `fpga/interface.cpp`: FPGA order-hook skeleton.
- `scripts/setup_ubuntu24.sh`: Bootstrap script for common HFT prerequisites.

## Quick start

```bash
bash infra/hft/scripts/setup_ubuntu24.sh
sudo python3 infra/hft/ebpf/run_probe.py
```

> **Warning**: DPDK NIC binding, XDP attach, and kernel tuning commands may interrupt network connectivity if run on production nodes without staged rollout.
