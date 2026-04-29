import random

import torch
from fastapi import FastAPI, WebSocket

from rl.agents import CostAgent, PlannerAgent, Router, SafetyAgent
from rl.planner import Planner
from rl.world_model import WorldModel

app = FastAPI()

wm = WorldModel()
planner = Planner(wm)
planner_agent = PlannerAgent(planner)
safety = SafetyAgent()
cost_agent = CostAgent()
router = Router()

STATE: dict[str, torch.Tensor] = {}


def get_state(t: str) -> torch.Tensor:
    if t not in STATE:
        STATE[t] = torch.tensor([200.0, 0.02, 0.5], dtype=torch.float32)
    return STATE[t]


@app.websocket("/ws/{tenant}")
async def ws(sock: WebSocket, tenant: str):
    await sock.accept()
    while True:
        s = get_state(tenant)
        s[0] *= random.uniform(0.95, 1.05)
        action = planner_agent.propose(s)
        final = router.decide(action, safety.allow(s), cost_agent.allow(s[2]))
        await sock.send_json({"state": s.tolist(), "action": final})
