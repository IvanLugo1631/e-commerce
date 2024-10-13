# app/routes/products.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models.product import Product
from schemas.product import Product as ProductSchema
import requests

router = APIRouter()

@router.get("/products", response_model=List[ProductSchema])
def get_products(db: Session = Depends(get_db), sort: str = None):
    products = db.query(Product).all()
    
    if sort == "price_low_to_high":
        products = sorted(products, key=lambda x: x.price)
    elif sort == "price_high_to_low":
        products = sorted(products, key=lambda x: x.price, reverse=True)
    
    return products

@router.get("/populate_products")
def populate_products(db: Session = Depends(get_db)) -> dict:
    try:
        response = requests.get("https://fakestoreapi.com/products")
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
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail="Failed to fetch products from fakestoreapi.com") from e
