import stripe
import os
from flask import redirect, request
from database import get_db

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

def create_checkout(plan):
    prices = {
        "pro": 500,     # $5
        "elite": 1500   # $15
    }

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            "price_data": {
                "currency": "usd",
                "product_data": {"name": f"DMR4 {plan.upper()}"},
                "unit_amount": prices[plan],
            },
            "quantity": 1,
        }],
        mode="payment",
        success_url=os.getenv("BASE_URL") + f"/success?plan={plan}",
        cancel_url=os.getenv("BASE_URL")
    )

    return redirect(session.url)

def activate_plan(user_id, plan):
    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "UPDATE users SET plan=%s WHERE id=%s",
        (plan, user_id)
    )

    conn.commit()
    cur.close()
    conn.close()