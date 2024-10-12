# app/routes/payment.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.cart import CartItem
import stripe
from fastapi import Request
import os
import logging

router = APIRouter()

# Get the Stripe secret key from environment variable
stripe_secret_key = os.getenv("STRIPE_SECRET_KEY")

# Set your secret key. Remember to switch to your live secret key in production.
stripe.api_key = stripe_secret_key

# Set up logging
logger = logging.getLogger(__name__)

@router.post("/create-payment-intent")
async def create_payment(db: Session = Depends(get_db)):
    cart_items = db.query(CartItem).all()
    total = sum(item.product.price * item.quantity for item in cart_items)

    try:
        intent = stripe.PaymentIntent.create(
            amount=int(total * 100),
            currency="usd",
        )
        logger.info("intent: %s", intent.client_secret)
        return {"clientSecret": intent.client_secret}
    except stripe.error.StripeError as e:
        logger.error("Stripe error: %s", str(e))
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error("Unexpected error: %s", str(e))
        raise HTTPException(status_code=500, detail="Unexpected error")