import os

from ledger.adapters.bank_adapter import BankAdapter
from ledger.adapters.stripe_adapter import StripeAdapter

ADAPTERS = {
    "stripe": StripeAdapter(os.getenv("STRIPE_SECRET_KEY", "sk_live_xxx")),
    "bank": BankAdapter(),
}


def charge(method: str, account: str, amount: float):
    return ADAPTERS[method].charge(account, amount)


def payout(method: str, account: str, amount: float):
    return ADAPTERS[method].payout(account, amount)
