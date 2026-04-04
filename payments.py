import stripe
import os
from flask import redirect

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

def create_checkout():
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            "price_data": {
                "currency": "usd",
                "product_data": {
                    "name": "DMR4 PRO"
                },
                "unit_amount": 500,
            },
            "quantity": 1,
        }],
        mode="payment",
        success_url=os.getenv("BASE_URL") + "/success",
        cancel_url=os.getenv("BASE_URL")
    )

    return redirect(session.url)