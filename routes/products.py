# app/routes/products.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models.product import Product
from schemas.product import Product as ProductSchema
from cachetools import TTLCache
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from fastapi.responses import ORJSONResponse
import httpx
import asyncio

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)
router.state.limiter = limiter
router.add_exception_handler(limiter.RateLimitExceeded, _rate_limit_exceeded_handler)

# Create a cache that stores up to 100 items and expires items after 60 seconds
cache = TTLCache(maxsize=100, ttl=60)

@router.get("/products", response_model=List[ProductSchema])
@limiter.limit("10/minute")  # Rate limit to 10 requests per minute
async def get_products(skip: int = 0, limit: int = 100, sort: str = None, db: Session = Depends(get_db)):
    cache_key = f"{skip}-{limit}-{sort}"
    if cache_key in cache:
        return cache[cache_key]
    else:
        query = db.query(Product).offset(skip).limit(limit)
        if sort == "price_low_to_high":
            query = query.order_by(Product.price)
        elif sort == "price_high_to_low":
            query = query.order_by(Product.price.desc())
        products = query.all()
        cache[cache_key] = products
        return products

@router.get("/populate_products")
async def populate_products(db: Session = Depends(get_db)) -> dict:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("https://fakestoreapi.com/products")
        response.raise_for_status()
        products_data = response.json()
        with db.begin():
            for product_data in products_data:
                product = Product(
                    id=product_data['id'],
                    title=product_data['title'],
                    price=product_data['price'],
                    description=product_data['description'],
                    category=product_data['category'],
                    image=product_data['image']
                )
                db.add(product)
        return {"message": "Products populated successfully"}
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=500, detail="Failed to fetch products from fakestoreapi.com") from e