"""Governance helper for market actions."""

from app.aiops.governance.voting import Voting


class Governor:
    def __init__(self, threshold: float = 0.6) -> None:
        self.voting = Voting(threshold=threshold)

    def cast(self, agent: str, decision: bool, weight: float = 1.0) -> None:
        self.voting.vote(agent=agent, decision=decision, weight=weight)

    def approved(self) -> bool:
        return self.voting.result()
