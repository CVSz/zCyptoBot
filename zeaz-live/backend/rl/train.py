from pathlib import Path

import torch

from rl.model import PolicyNet


def train(data, out_path: str = "policy.pt"):
    model = PolicyNet()
    opt = torch.optim.Adam(model.parameters(), lr=1e-3)

    for s, a, r in data:
        x = torch.tensor([s["latency"], s["error"], s["load"]], dtype=torch.float32)
        probs = model(x)

        loss = -torch.log(probs[a].clamp_min(1e-8)) * r
        opt.zero_grad()
        loss.backward()
        opt.step()

    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    torch.save(model.state_dict(), out_path)
