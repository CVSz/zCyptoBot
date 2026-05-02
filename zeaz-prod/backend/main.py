import asyncio
import random

from fastapi import FastAPI, HTTPException, WebSocket
from fastapi.security import HTTPAuthorizationCredentials

from auth import create_token, verify_credentials
from db import init_db, save_decision
from explain import explain
from kafka import publish
from redis_client import cache_set, publish as redis_publish
from rl.agent import RLAgent

app = FastAPI()
agent = RLAgent()
STATE: dict[str, dict[str, float]] = {}


@app.on_event("startup")
async def startup() -> None:
    init_db()


@app.post("/auth/token")
async def token(user: str, tenant: str) -> dict:
    return {"token": create_token(user, tenant)}


def get_state(tenant: str) -> dict[str, float]:
    if tenant not in STATE:
        STATE[tenant] = {"latency": 200.0, "error": 0.02, "load": 0.5}
    return STATE[tenant]


@app.websocket("/ws/{tenant}")
async def ws(tenant: str, ws: WebSocket, token: str) -> None:
    claims = verify_credentials(HTTPAuthorizationCredentials(scheme="Bearer", credentials=token))
    if claims.get("tenant") != tenant:
        raise HTTPException(403, "tenant mismatch")

    await ws.accept()
    while True:
        state = get_state(tenant)
        state["latency"] *= random.uniform(0.95, 1.05)
        state["error"] *= random.uniform(0.95, 1.05)

        action = agent.act(state)
        reward = 1.0 - state["latency"] / 300
        agent.update(state, action, reward)
        agent.replay_train(16)

        exp = explain(state, action)

        publish("decisions", {"tenant": tenant, "action": action, "reward": reward})
        redis_publish("stream", {"tenant": tenant, "state": state})
        cache_set(f"tenant:{tenant}:state", state)
        save_decision(tenant, action, reward)

        await ws.send_json({"state": state, "action": action, "explain": exp})
        await asyncio.sleep(1)
