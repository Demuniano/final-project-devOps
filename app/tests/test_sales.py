import pytest
from fastapi.testclient import TestClient


class TestSales:
    """Pruebas para endpoints de ventas"""
    
    def test_create_sale_success(self, client, setup_test_data):
        """Prueba crear venta exitosamente"""
        client_id = setup_test_data["client_id"]
        product_id = setup_test_data["product_id"]
        
        response = client.post("/sales", json={
            "client_id": client_id,
            "product_id": product_id,
            "quantity": 2
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Sale created successfully"
        assert "sale_id" in data
        assert "total_amount" in data
    
    def test_create_sale_invalid_client(self, client, setup_test_data):
        """Prueba crear venta con cliente inválido"""
        product_id = setup_test_data["product_id"]
        
        response = client.post("/sales", json={
            "client_id": "invalid_client",
            "product_id": product_id,
            "quantity": 1
        })
        
        assert response.status_code == 400
        assert "Client not found" in response.json()["detail"]
    
    def test_create_sale_invalid_product(self, client, setup_test_data):
        """Prueba crear venta con producto inválido"""
        client_id = setup_test_data["client_id"]
        
        response = client.post("/sales", json={
            "client_id": client_id,
            "product_id": "invalid_product",
            "quantity": 1
        })
        
        assert response.status_code == 400
        assert "Product not found" in response.json()["detail"]
    
    def test_create_sale_insufficient_stock(self, client, setup_test_data):
        """Prueba crear venta con stock insuficiente"""
        client_id = setup_test_data["client_id"]
        product_id = setup_test_data["product_id"]
        
        response = client.post("/sales", json={
            "client_id": client_id,
            "product_id": product_id,
            "quantity": 100  # Más del stock disponible
        })
        
        assert response.status_code == 400
        assert "Insufficient stock" in response.json()["detail"]
    
    def test_create_sale_invalid_quantity(self, client, setup_test_data):
        """Prueba crear venta con cantidad inválida"""
        client_id = setup_test_data["client_id"]
        product_id = setup_test_data["product_id"]
        
        response = client.post("/sales", json={
            "client_id": client_id,
            "product_id": product_id,
            "quantity": 0
        })
        
        assert response.status_code == 400
        assert "Quantity must be greater than 0" in response.json()["detail"]
    
    def test_get_sales(self, client, setup_test_data):
        """Prueba obtener lista de ventas"""
        client_id = setup_test_data["client_id"]
        product_id = setup_test_data["product_id"]
        
        # Crear una venta primero
        client.post("/sales", json={
            "client_id": client_id,
            "product_id": product_id,
            "quantity": 1
        })
        
        response = client.get("/sales")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
    
    def test_get_sale_by_id(self, client, setup_test_data):
        """Prueba obtener venta por ID"""
        client_id = setup_test_data["client_id"]
        product_id = setup_test_data["product_id"]
        
        # Crear venta
        create_response = client.post("/sales", json={
            "client_id": client_id,
            "product_id": product_id,
            "quantity": 1
        })
        sale_id = create_response.json()["sale_id"]
        
        # Obtener venta
        response = client.get(f"/sales/{sale_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["client_id"] == client_id
        assert data["product_id"] == product_id
    
    def test_get_sale_not_found(self, client):
        """Prueba obtener venta que no existe"""
        response = client.get("/sales/nonexistent")
        assert response.status_code == 404
        assert "Sale not found" in response.json()["detail"]
    
    def test_get_sales_by_client(self, client, setup_test_data):
        """Prueba obtener ventas por cliente"""
        client_id = setup_test_data["client_id"]
        product_id = setup_test_data["product_id"]
        
        # Crear venta
        client.post("/sales", json={
            "client_id": client_id,
            "product_id": product_id,
            "quantity": 1
        })
        
        response = client.get(f"/sales/client/{client_id}")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert all(sale["client_id"] == client_id for sale in data)
    
    def test_get_sales_by_product(self, client, setup_test_data):
        """Prueba obtener ventas por producto"""
        client_id = setup_test_data["client_id"]
        product_id = setup_test_data["product_id"]
        
        # Crear venta
        client.post("/sales", json={
            "client_id": client_id,
            "product_id": product_id,
            "quantity": 1
        })
        
        response = client.get(f"/sales/product/{product_id}")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert all(sale["product_id"] == product_id for sale in data)
    
    def test_stock_update_after_sale(self, client, setup_test_data):
        """Prueba que el stock se actualice después de una venta"""
        client_id = setup_test_data["client_id"]
        product_id = setup_test_data["product_id"]
        
        # Obtener stock inicial
        initial_response = client.get(f"/products/{product_id}")
        initial_stock = initial_response.json()["stock"]
        
        # Crear venta
        quantity = 2
        client.post("/sales", json={
            "client_id": client_id,
            "product_id": product_id,
            "quantity": quantity
        })
        
        # Verificar stock actualizado
        final_response = client.get(f"/products/{product_id}")
        final_stock = final_response.json()["stock"]
        
        assert final_stock == initial_stock - quantity
