"""Weighted quorum voting."""


class Voting:
    def __init__(self, threshold: float = 0.6, min_quorum: int = 1) -> None:
        self.votes: dict[str, tuple[bool, float]] = {}
        self.threshold = threshold
        self.min_quorum = min_quorum

    def vote(self, agent: str, decision: bool, weight: float = 1.0) -> None:
        self.votes[agent] = (decision, max(0.0, weight))

    def result(self) -> bool:
        if len(self.votes) < self.min_quorum:
            return False
        yes_weight = sum(w for d, w in self.votes.values() if d)
        total_weight = sum(w for _, w in self.votes.values())
        if total_weight == 0:
            return False
        return (yes_weight / total_weight) >= self.threshold
