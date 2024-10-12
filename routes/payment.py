# app/routes/payment.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.cart import CartItem
import stripe
from fastapi import Request

router = APIRouter()

# Set your secret key. Remember to switch to your live secret key in production.
stripe.api_key = "sk_test_51Q9CG92MT9PgHVjwdeUUG9v3Jp0VlWAcp3WbI91AJo8YPpm8N7TNqrov2yihadO2Fuh01NAhiJCAro1BHwnkopb400QLOaI2Lc"

@router.post("/create-payment-intent")
async def create_payment(db: Session = Depends(get_db)):
    cart_items = db.query(CartItem).all()
    total = sum(item.product.price * item.quantity for item in cart_items)

    try:
        intent = stripe.PaymentIntent.create(
            amount=int(total * 100),
            currency="usd",
        )
        print("intent", intent.client_secret)
        return {"clientSecret": intent.client_secret}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))