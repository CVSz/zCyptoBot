"""Escrow flow for job-based credit settlement."""

from economy.credits.ledger import BAL, spend

ESCROW = {}


def lock(job_id: str, user: str, amount: float) -> None:
    """Lock user credits into escrow for a job."""
    spend(user, amount)
    ESCROW[job_id] = amount


def release(job_id: str, provider: str) -> None:
    """Release escrowed credits to the provider."""
    amt = ESCROW.pop(job_id, 0)
    BAL[provider] += amt
