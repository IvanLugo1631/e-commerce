
# app/schemas/cart.py
from pydantic import BaseModel, ConfigDict
from .product import Product

class CartItemBase(BaseModel):
    product_id: int
    quantity: int

class CartItemCreate(CartItemBase):
    pass

class CartItem(CartItemBase):
    id: int
    product: Product

    class Config(ConfigDict):
        from_attributes = True