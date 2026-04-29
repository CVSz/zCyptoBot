import asyncio

from fastapi import FastAPI, WebSocket

from engine import Engine
from stream import update_state
from tenant import get_tenant_state

app = FastAPI()
engine = Engine()


@app.get("/metrics/{tenant}")
def metrics(tenant: str):
    return get_tenant_state(tenant)


@app.get("/decision/{tenant}")
def decision(tenant: str):
    state = get_tenant_state(tenant)
    return {"action": engine.decide(state)}


@app.websocket("/ws/{tenant}")
async def ws(ws: WebSocket, tenant: str):
    await ws.accept()
    while True:
        state = get_tenant_state(tenant)
        state = update_state(state)
        action = engine.decide(state)

        await ws.send_json({"metrics": state, "decision": action})
        await asyncio.sleep(1)
