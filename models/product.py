# app/models/product.py
from sqlalchemy import Column, Integer, String, Float
from database import Base
from sqlalchemy.orm import relationship


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    price = Column(Float)
    description = Column(String)
    category = Column(String)
    image = Column(String)    
    cart_items = relationship("CartItem", back_populates="product")


