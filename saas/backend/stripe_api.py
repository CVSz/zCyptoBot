import os

import stripe
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()
stripe.api_key = os.getenv("STRIPE_SECRET_KEY", "")


class CheckoutBody(BaseModel):
    plan: str = "pro"


@router.post("/create-checkout")
def create_checkout(payload: CheckoutBody):
    if not stripe.api_key:
        raise HTTPException(500, "Missing STRIPE_SECRET_KEY")

    price_id = os.getenv("STRIPE_PRICE_PRO") if payload.plan == "pro" else os.getenv("STRIPE_PRICE_BASIC")
    if not price_id:
        raise HTTPException(500, "Missing Stripe price id for selected plan")

    session = stripe.checkout.Session.create(
        mode="subscription",
        line_items=[{"price": price_id, "quantity": 1}],
        success_url=os.getenv("STRIPE_SUCCESS_URL", "http://localhost:3000/success"),
        cancel_url=os.getenv("STRIPE_CANCEL_URL", "http://localhost:3000/billing"),
    )
    return {"url": session.url}
