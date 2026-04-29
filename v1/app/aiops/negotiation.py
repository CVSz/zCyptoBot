from dataclasses import dataclass, field
from typing import Dict, Iterable, List


@dataclass
class Proposal:
    action: str
    score: float
    constraints: Dict[str, bool] = field(default_factory=dict)


class NegotiationEngine:
    """Auction/voting hybrid with strict feasibility filtering."""

    def __init__(self, agents: Iterable[object]):
        self.agents = list(agents)

    def negotiate(self, state: dict) -> str:
        proposals: List[Proposal] = []
        for agent in self.agents:
            proposal = agent.propose(state)
            if proposal is not None:
                proposals.append(proposal)

        if not proposals:
            return "hold"

        feasible = [p for p in proposals if all(p.constraints.values())]
        if not feasible:
            return "hold"

        # combine auction score (primary) and light vote count by action (secondary)
        votes: Dict[str, int] = {}
        for proposal in feasible:
            votes[proposal.action] = votes.get(proposal.action, 0) + 1

        return max(feasible, key=lambda p: (p.score, votes[p.action])).action
