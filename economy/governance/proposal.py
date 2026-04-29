"""Proposal registry for governance actions."""

PROPOSALS = {}


def create(pid: str, change):
    PROPOSALS[pid] = {"change": change, "votes": []}
