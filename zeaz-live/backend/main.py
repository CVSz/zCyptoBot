import asyncio
import random
from pathlib import Path

import torch
from fastapi import Depends, FastAPI, Header, HTTPException, WebSocket

from auth import verify
from billing import get_usage, track
from feature_store.offline import insert
from feature_store.online import put
from rbac import check
from rl.model import ACTIONS, PolicyNet

app = FastAPI()

model = PolicyNet()
policy_path = Path("policy.pt")
if policy_path.exists():
    model.load_state_dict(torch.load(policy_path, map_location="cpu"))

STATE = {}


def require_auth(authorization: str = Header(default="")) -> dict:
    if not authorization.startswith("Bearer "):
        raise HTTPException(401, "Missing bearer token")
    return verify(authorization.replace("Bearer ", "", 1))


def get_state(t: str):
    if t not in STATE:
        STATE[t] = {"latency": 200.0, "error": 0.02, "load": 0.5}
    return STATE[t]


@app.get("/metrics/{tenant}")
def metrics(tenant: str, claims: dict = Depends(require_auth)):
    if claims.get("tenant") != tenant:
        raise HTTPException(403, "Tenant mismatch")
    return {"tenant": tenant, "usage": get_usage(tenant), "state": get_state(tenant)}


@app.get("/admin/usage/{tenant}")
def admin_usage(tenant: str, claims: dict = Depends(require_auth)):
    if not check(claims["role"], "admin"):
        raise HTTPException(403, "admin required")
    return {"tenant": tenant, "usage": get_usage(tenant)}


@app.websocket("/ws/{tenant}")
async def ws(ws: WebSocket, tenant: str):
    await ws.accept()
    while True:
        s = get_state(tenant)
        s["latency"] *= random.uniform(0.95, 1.05)
        s["error"] *= random.uniform(0.95, 1.05)

        x = torch.tensor([s["latency"], s["error"], s["load"]], dtype=torch.float32)
        probs = model(x)
        a = ACTIONS[int(torch.argmax(probs))]

        cost = s["load"] * 0.1
        track(tenant, cost)
        put(tenant, s)

        try:
            insert(tenant, s)
        except Exception as exc:  # noqa: BLE001
            await ws.send_json({"offline_insert_error": str(exc)})

        await ws.send_json({"state": s, "action": a, "cost": cost, "usage_total": get_usage(tenant)})
        await asyncio.sleep(1)
