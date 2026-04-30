"""Stripe checkout and subscription helpers."""

import os

import stripe

stripe.api_key = os.getenv("STRIPE_SECRET_KEY", "")


def create_subscription(customer_id: str, price_id: str):
    """Create a Stripe subscription in incomplete state for payment confirmation."""
    return stripe.Subscription.create(
        customer=customer_id,
        items=[{"price": price_id}],
        payment_behavior="default_incomplete",
        expand=["latest_invoice.payment_intent"],
    )
