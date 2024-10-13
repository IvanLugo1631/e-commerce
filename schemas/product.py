# app/schemas/product.py
from pydantic import BaseModel, ConfigDict

class ProductBase(BaseModel):
    title: str
    price: float
    description: str
    category: str
    image: str

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int

    class Config(ConfigDict):
        from_attributes = True