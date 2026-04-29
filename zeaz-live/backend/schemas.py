from pydantic import BaseModel


class Metrics(BaseModel):
    latency: float
    error: float
    load: float


class Decision(BaseModel):
    action: str
    tenant: str
