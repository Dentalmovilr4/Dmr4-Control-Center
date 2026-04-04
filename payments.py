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
                "unit_amount": 500,  # $5
            },
            "quantity": 1,
        }],
        mode="payment",
        success_url="http://localhost:5000/success",
        cancel_url="http://localhost:5000"
    )

    return redirect(session.url)