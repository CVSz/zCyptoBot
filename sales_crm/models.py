from dataclasses import dataclass
from typing import List


@dataclass
class Deal:
    id: str
    company: str
    stage: str  # lead, qualified, demo, pilot, closed
    value: float
    probability: float


@dataclass
class Activity:
    deal_id: str
    type: str  # call, email, demo
    note: str


DEALS: List[Deal] = []
ACTIVITIES: List[Activity] = []
