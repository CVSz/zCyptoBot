from decentralized.fairness.drf import pick_min_dominant
from decentralized.fairness.quota import allow
from decentralized.p2p.peer_store import list_peers
from decentralized.trust.byzantine import filter_outliers
from decentralized.trust.scoring import get as trust_score
from decentralized.zk.audit import append
from decentralized.zk.commit import commit


class FederatedScheduler:
    def select(self, tenant: str, demand: dict, kpi_samples: dict):
        latencies = filter_outliers(kpi_samples.get("latency", []))

        peers = list_peers()
        cands = []
        for nid, meta in peers.items():
            if not allow(tenant, demand.get("units", 0)):
                continue
            cands.append(
                {
                    "node_id": nid,
                    "usage": meta.get("usage", {"cpu": 0.1, "mem": 0.1}),
                    "capacity": meta.get("capacity", {"cpu": 1.0, "mem": 1.0}),
                    "trust": trust_score(nid),
                    "lat": sum(latencies) / len(latencies) if latencies else meta.get("latency", 200),
                }
            )

        if not cands:
            return None

        pick = pick_min_dominant(cands)
        cands.sort(key=lambda c: (c["node_id"] != pick, -c["trust"], c["lat"]))
        chosen = cands[0]["node_id"]

        # quote = meta["quote"]
        # assert verify_quote(quote, expected_mrenclave="abc...")

        return chosen

    def audit_decision(self, payload: dict, salt: str):
        h = commit(payload, salt)
        return append(h)
