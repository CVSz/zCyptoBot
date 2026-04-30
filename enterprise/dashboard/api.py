"""FastAPI routes for enterprise dashboard."""

from fastapi import APIRouter

from .calculator import compute_metrics

router = APIRouter()


@router.get("/dashboard")
def dashboard():
    """Return sample dashboard metrics; replace with real billing/CUR data."""
    return compute_metrics(usage_cost=10000, zeaz_cost=7000, revenue=12000)
