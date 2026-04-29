import uuid

from decentralized.k8s.deploy_job import deploy
from decentralized.ledger.accounts import debit
from decentralized.ledger.escrow import lock
from decentralized.market.matching import match
from decentralized.market.orderbook import Order, OrderBook


class Scheduler:
    def __init__(self):
        self.ob = OrderBook()

    def submit_job(self, tenant: str, price: float, qty: float):
        oid = str(uuid.uuid4())
        self.ob.add(Order(order_id=oid, side="buy", price=price, qty=qty))
        return oid

    def add_provider(self, node_id: str, price: float, qty: float):
        self.ob.add(
            Order(order_id=f"ask-{node_id}", side="sell", price=price, qty=qty, node_id=node_id)
        )

    def run(self, payer: str):
        trades = match(self.ob)
        results = []
        for t in trades:
            job_id = t["buyer"]
            provider = t["seller"]
            total_cost = t["price"] * t["qty"]

            # escrow
            lock(job_id, payer, total_cost, debit)

            # execute
            deploy(provider, job_id, t["qty"])

            results.append({**t, "job_id": job_id, "cost": total_cost})
        return results
