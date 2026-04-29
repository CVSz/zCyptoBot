from dataclasses import dataclass


@dataclass
class K8sAction:
    action: str
    namespace: str = "zeaz"


class K8sClient:
    def apply_action(self, action: str) -> K8sAction:
        return K8sAction(action=action)
