import threading
import time
import uuid

from decentralized.p2p.gossip import publish, subscribe
from decentralized.p2p.peer_store import add_peer

NODE_ID = f"node-{uuid.uuid4().hex[:8]}"


def on_msg(msg):
    if msg["topic"] == "peer.announce":
        add_peer(msg["payload"]["peer_id"], msg["payload"])


def start():
    subscribe(on_msg)

    def loop():
        while True:
            publish("peer.announce", {"peer_id": NODE_ID, "ts": time.time()})
            time.sleep(5)

    t = threading.Thread(target=loop, daemon=True)
    t.start()
