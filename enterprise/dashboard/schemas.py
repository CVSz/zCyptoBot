"""Pydantic schemas for enterprise dashboard payloads."""

from pydantic import BaseModel


class DashboardMetrics(BaseModel):
    original_cost: float
    zeaz_cost: float
    savings: float
    roi: float
    margin: float
