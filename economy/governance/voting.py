"""Voting operations over proposals."""

from economy.governance.proposal import PROPOSALS


def vote(pid: str, voter: str, approve: bool) -> None:
    PROPOSALS[pid]["votes"].append((voter, approve))


def result(pid: str) -> bool:
    votes = PROPOSALS[pid]["votes"]
    yes = sum(1 for _, v in votes if v)
    return yes > len(votes) / 2
