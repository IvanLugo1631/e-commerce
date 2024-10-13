
# app/routes/cart.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models.cart import CartItem
from schemas.cart import CartItem as CartItemSchema, CartItemCreate
from models.product import Product
from cachetools import TTLCache
from sqlalchemy import func

# Create a cache that stores up to 100 items and expires items after 60 seconds
cache = TTLCache(maxsize=100, ttl=60)
router = APIRouter()

@router.post("/cart/add", response_model=CartItemSchema)
def add_to_cart(item: CartItemCreate, db: Session = Depends(get_db)):
    db_item = db.query(CartItem).filter(CartItem.product_id == item.product_id).first()
    if db_item:
        raise HTTPException(status_code=400, detail="Item already exists in the cart")
    db_item = CartItem(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/cart", response_model=List[CartItemSchema])
def get_cart(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # Use the cache key as the combination of skip and limit
    cache_key = f"{skip}-{limit}"
    if cache_key in cache:
        return cache[cache_key]
    else:
        items = db.query(CartItem).offset(skip).limit(limit).all()
        cache[cache_key] = items
        return items

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
    total = db.query(func.sum(CartItem.quantity * Product.price))\
    .join(Product, CartItem.product_id == Product.id)\
    .scalar()    
    return {"total": total}