import pytest
from fastapi.testclient import TestClient
from main import app

@pytest.fixture
def client():
    return TestClient(app)

def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the E-commerce API"}

def test_get_products(client):
    response = client.get("/products")
    assert response.status_code == 200
    # Add more assertions based on your expected response

def test_get_cart(client):
    response = client.get("/cart")
    assert response.status_code == 200
    # Add more assertions based on your expected response

def test_get_payment(client):
    response = client.post("/create-payment-intent")
    assert response.status_code == 200
    # Add more assertions based on your expected response

def test_get_cart_total(client):
    response = client.get("/cart/total")
    assert response.status_code == 200
    # Add more assertions based on your expected response