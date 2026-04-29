from pathlib import Path

import torch

from app.ai.agent import DQN


class RLInference:
    def __init__(self):
        self.model = DQN(4, 3)
        model_path = Path("app/models/policy.pt")
        if model_path.exists():
            self.model.load_state_dict(torch.load(model_path, map_location="cpu"))
        self.model.eval()

    def predict(self, state):
        with torch.no_grad():
            q = self.model(torch.tensor(state, dtype=torch.float32))
            action = torch.argmax(q).item()

        return ["HOLD", "LONG", "SHORT"][action]
