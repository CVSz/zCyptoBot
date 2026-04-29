from .accounts import credit
from .escrow import release


def settle_success(job_id: str, provider: str):
    release(job_id, provider, credit)


def settle_refund(job_id: str, payer: str):
    from .escrow import refund

    refund(job_id, payer, credit)
