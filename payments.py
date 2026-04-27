import stripe
import os
from dotenv import load_dotenv

load_dotenv()
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

PRICE_ID = "price_1TQOjN9kxypFQX5lcogqnsv6"
SUCCESS_URL = os.getenv("BASE_URL", "https://keyword-monitor-production.up.railway.app") + "/success"
CANCEL_URL = os.getenv("BASE_URL", "https://keyword-monitor-production.up.railway.app") + "/cancel"

def create_checkout_session(email):
    """创建Stripe支付页面"""
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        mode="subscription",
        customer_email=email,
        line_items=[{"price": PRICE_ID, "quantity": 1}],
        success_url=SUCCESS_URL + "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=CANCEL_URL,
    )
    return session.url

def is_paid_user(email):
    """检查邮箱是否有有效订阅"""
    customers = stripe.Customer.list(email=email, limit=1)
    if not customers.data:
        return False
    customer_id = customers.data[0].id
    subscriptions = stripe.Subscription.list(
        customer=customer_id,
        status="active",
        limit=1
    )
    return len(subscriptions.data) > 0