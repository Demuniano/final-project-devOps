import pytest
from fastapi.testclient import TestClient
from app import app

@pytest.fixture
def client():
    """Fixture para el cliente de pruebas"""
    return TestClient(app)

@pytest.fixture
def sample_client_data():
    """Datos de ejemplo para un cliente"""
    return {
        "name": "Juan Pérez",
        "email": "juan@email.com",
        "phone": "+1234567890"
    }

@pytest.fixture
def sample_product_data():
    """Datos de ejemplo para un producto"""
    return {
        "name": "Laptop Gaming",
        "price": 1299.99,
        "description": "Laptop para gaming de alta gama",
        "stock": 10
    }

@pytest.fixture
def sample_sale_data():
    """Datos de ejemplo para una venta"""
    return {
        "quantity": 2
    }

@pytest.fixture
def setup_test_data(client):
    """Fixture que configura datos de prueba"""
    # Crear cliente
    client_response = client.post("/clients", json={
        "name": "Test Client",
        "email": "test@email.com"
    })
    client_id = client_response.json()["client_id"]
    
    # Crear producto
    product_response = client.post("/products", json={
        "name": "Test Product",
        "price": 99.99,
        "stock": 5
    })
    product_id = product_response.json()["product_id"]
    
    return {
        "client_id": client_id,
        "product_id": product_id
    }
