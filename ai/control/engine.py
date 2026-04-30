"""Core control engine for autonomous global routing and pricing decisions."""

from __future__ import annotations

from dataclasses import dataclass
from statistics import mean
from typing import Iterable, Protocol


class Agent(Protocol):
    def propose(self, state: dict) -> float:
        """Return a normalized action score for current state."""


@dataclass
class ControlSystem:
    """Aggregate multi-agent proposals into a single control decision."""

    world_model: object
    agents: Iterable[Agent]

    def decide(self, state: dict) -> float:
        proposals = [agent.propose(state) for agent in self.agents]
        if not proposals:
            raise ValueError("ControlSystem requires at least one agent")
        return mean(proposals)
