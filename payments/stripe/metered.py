"""Usage-based billing helpers for Stripe metered products."""

import time

import stripe


def report_usage(subscription_item_id, quantity):
    """Report metered usage to Stripe."""
    return stripe.UsageRecord.create(
        subscription_item=subscription_item_id,
        quantity=quantity,
        timestamp=int(time.time()),
        action="increment",
    )
