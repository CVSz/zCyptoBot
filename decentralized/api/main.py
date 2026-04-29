from fastapi import FastAPI

from decentralized.coordinator.scheduler import Scheduler
from decentralized.ledger.accounts import balance, create_account, credit
from decentralized.registry.node_registry import list_nodes, register

app = FastAPI()
sched = Scheduler()


@app.post("/node/register")
def node_register(node_id: str, cpu: float, mem: float, price: float, latency: float):
    register(node_id, {"cpu": cpu, "mem": mem, "price": price, "latency": latency})
    sched.add_provider(node_id, price=price, qty=cpu)
    return {"ok": True}


@app.get("/nodes")
def nodes():
    return list_nodes()


@app.post("/account/create")
def acc_create(user: str):
    create_account(user)
    return {"ok": True}


@app.post("/account/fund")
def acc_fund(user: str, amount: float):
    credit(user, amount)
    return {"balance": balance(user)}


@app.post("/job/submit")
def job_submit(user: str, price: float, qty: float):
    oid = sched.submit_job(user, price, qty)
    trades = sched.run(payer=user)
    return {"order_id": oid, "trades": trades}
