# app/main.py
from fastapi import FastAPI
from routes import products, cart, payment
from database import engine, Base
import uvicorn

app = FastAPI()

# Create database tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(products.router)
app.include_router(cart.router)
app.include_router(payment.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the backend of the E-commerce "}

    if __name__ == "__main__":
        uvicorn.run(app, host="0.0.0.0", port=8000)