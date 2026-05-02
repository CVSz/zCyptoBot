import asyncio
import os
import random
from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException, WebSocket
from fastapi.middleware.cors import CORSMiddleware

from auth import create_token, verify_token
from stripe_api import router as stripe_router

app = FastAPI(title="ZEAZ SaaS API", version="1.0.0")
app.include_router(stripe_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/auth/signup")
def signup(email: str, tenant: str):
    token = create_token(user={"email": email, "tenant": tenant, "role": "owner"})
    return {"access_token": token, "token_type": "bearer"}


@app.get("/auth/me")
def me(token: str):
    try:
        return verify_token(token)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(401, "Invalid token") from exc


@app.websocket("/ws/metrics")
async def ws_metrics(ws: WebSocket):
    await ws.accept()
    revenue = 1500
    users = 48
    while True:
        revenue += random.randint(10, 40)
        users = max(1, users + random.randint(-2, 4))
        await ws.send_json(
            {
                "ts": datetime.now(timezone.utc).isoformat(),
                "latency": random.randint(40, 180),
                "revenue": revenue,
                "active_users": users,
            }
        )
        await asyncio.sleep(1)


@app.get("/healthz")
def healthz():
    return {"ok": True, "stripe": bool(os.getenv("STRIPE_SECRET_KEY"))}
