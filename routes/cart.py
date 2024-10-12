
# app/routes/cart.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models.cart import CartItem
from schemas.cart import CartItem as CartItemSchema, CartItemCreate
from models.product import Product

router = APIRouter()

@router.post("/cart/add", response_model=CartItemSchema)
def add_to_cart(item: CartItemCreate, db: Session = Depends(get_db)):
    db_item = CartItem(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/cart", response_model=List[CartItemSchema])
def get_cart(db: Session = Depends(get_db)):
    return db.query(CartItem).all()

@router.put("/cart/{item_id}", response_model=CartItemSchema)
def update_cart_item(item_id: int, quantity: int, db: Session = Depends(get_db)):
    db_item = db.query(CartItem).filter(CartItem.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    db_item.quantity = quantity
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/cart/total")
def get_cart_total(db: Session = Depends(get_db)):
    cart_items = db.query(CartItem).all()
    total = sum(item.product.price * item.quantity for item in cart_items)
    return {"total": total}