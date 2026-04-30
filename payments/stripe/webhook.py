"""Stripe webhook handling utilities."""

import os

import stripe

endpoint_secret = os.getenv("STRIPE_WEBHOOK_SECRET", "")


def handle(event):
    """Map Stripe invoice events to account actions."""
    if event["type"] == "invoice.paid":
        return "activate_account"

    if event["type"] == "invoice.payment_failed":
        return "suspend_account"

    return "ignore"
