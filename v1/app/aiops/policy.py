from dataclasses import dataclass


@dataclass
class Policy:
    id: str
    version: str
    params: dict


class PolicyRegistry:
    def __init__(self):
        self.store = {}

    def register(self, policy: Policy):
        self.store[(policy.id, policy.version)] = policy

    def get(self, policy_id: str, version: str):
        return self.store[(policy_id, version)]
