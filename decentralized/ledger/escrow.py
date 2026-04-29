ESCROW = {}  # job_id -> amount


def lock(job_id: str, payer: str, amount: float, debit_fn):
    debit_fn(payer, amount)
    ESCROW[job_id] = amount


def release(job_id: str, payee: str, credit_fn):
    amt = ESCROW.pop(job_id, 0.0)
    credit_fn(payee, amt)


def refund(job_id: str, payer: str, credit_fn):
    amt = ESCROW.pop(job_id, 0.0)
    credit_fn(payer, amt)
