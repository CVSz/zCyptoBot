import uuid


class Evolution:
    def __init__(self, registry: dict) -> None:
        self.registry = registry

    def propose(self, base_policy: str, tweaks: dict) -> dict:
        new_id = str(uuid.uuid4())
        new_policy = {
            "id": new_id,
            "base": base_policy,
            "params": tweaks,
        }
        self.registry[new_id] = new_policy
        return new_policy

    def promote(self, policy_id: str) -> None:
        self.registry["active"] = policy_id

    def rollback(self, previous_policy_id: str) -> None:
        self.registry["active"] = previous_policy_id
