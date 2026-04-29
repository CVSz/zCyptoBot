from typing import Dict, List

NODES: Dict[str, dict] = {}


def register(node_id: str, meta: dict):
    # meta: {region, cpu, mem, price_cpu, price_mem, latency}
    NODES[node_id] = meta


def list_nodes() -> List[dict]:
    return [{"node_id": k, **v} for k, v in NODES.items()]


def get(node_id: str) -> dict:
    return NODES[node_id]
