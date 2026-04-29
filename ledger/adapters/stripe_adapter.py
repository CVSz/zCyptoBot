from .base import Adapter

try:
    import stripe
except ImportError:  # pragma: no cover
    stripe = None


class StripeAdapter(Adapter):
    def __init__(self, key: str):
        self.key = key
        if stripe is not None:
            stripe.api_key = key

    def charge(self, account: str, amount: float):
        if stripe is None:
            return {
                "status": "stubbed",
                "provider": "stripe",
                "account": account,
                "amount": amount,
            }
        return stripe.PaymentIntent.create(
            amount=int(amount * 100),
            currency="usd",
            metadata={"account": account},
        )

    def payout(self, account: str, amount: float):
        return {"status": "queued", "provider": "stripe", "account": account, "amount": amount}
