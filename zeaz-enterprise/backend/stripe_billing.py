import os
from datetime import datetime, timezone

import stripe

stripe.api_key = os.getenv("STRIPE_SECRET_KEY", "")


class StripeConfigError(RuntimeError):
    pass


def _ensure_api_key() -> None:
    if not stripe.api_key:
        raise StripeConfigError("STRIPE_SECRET_KEY is not configured")


def create_customer(email: str) -> stripe.Customer:
    _ensure_api_key()
    return stripe.Customer.create(email=email)


def create_subscription(customer_id: str, price_id: str) -> stripe.Subscription:
    _ensure_api_key()
    return stripe.Subscription.create(customer=customer_id, items=[{"price": price_id}])


def report_usage(subscription_item_id: str, quantity: int) -> stripe.UsageRecord:
    _ensure_api_key()
    return stripe.UsageRecord.create(
        subscription_item=subscription_item_id,
        quantity=quantity,
        timestamp=int(datetime.now(tz=timezone.utc).timestamp()),
        action="increment",
    )
