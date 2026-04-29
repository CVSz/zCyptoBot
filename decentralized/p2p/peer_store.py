from typing import Dict

PEERS: Dict[str, dict] = {}


def add_peer(peer_id: str, meta: dict):
    PEERS[peer_id] = meta


def list_peers():
    return PEERS
