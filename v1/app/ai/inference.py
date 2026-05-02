from pathlib import Path
import logging
import torch

from app.ai.agent import DQN

logger = logging.getLogger(__name__)


class RLInference:
    def __init__(self):
        self.model = DQN(4, 3)
        model_path = Path("app/models/policy.pt")
        if model_path.exists():
            try:
                # torch.load can execute arbitrary code when loading untrusted pickles.
                # Ensure the loaded object looks like a state_dict before applying it.
                data = torch.load(model_path, map_location="cpu")
                if isinstance(data, dict):
                    self.model.load_state_dict(data)
                else:
                    logger.warning("Model file %s did not contain a state_dict; skipping load", model_path)
            except Exception as e:
                logger.exception("Failed to load model from %s: %s", model_path, e)
        self.model.eval()

    def predict(self, state):
        with torch.no_grad():
            q = self.model(torch.tensor(state, dtype=torch.float32))
            action = torch.argmax(q).item()

        return ["HOLD", "LONG", "SHORT"][action]
