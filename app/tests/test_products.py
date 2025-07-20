import pytest
from fastapi.testclient import TestClient


class TestProducts:
    """Pruebas para endpoints de productos"""
    
    def test_create_product_success(self, client, sample_product_data):
        """Prueba crear producto exitosamente"""
        response = client.post("/products", json=sample_product_data)
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Product created successfully"
        assert "product_id" in data
    
    def test_create_product_invalid_price(self, client):
        """Prueba crear producto con precio inválido"""
        response = client.post("/products", json={
            "name": "Test Product",
            "price": -10,
            "stock": 5
        })
        assert response.status_code == 400
        assert "Product price must be greater than 0" in response.json()["detail"]
    
    def test_create_product_empty_name(self, client):
        """Prueba crear producto con nombre vacío"""
        response = client.post("/products", json={
            "name": "",
            "price": 100,
            "stock": 5
        })
        assert response.status_code == 400
        assert "Product name cannot be empty" in response.json()["detail"]
    
    def test_get_products(self, client, sample_product_data):
        """Prueba obtener lista de productos"""
        # Crear un producto primero
        client.post("/products", json=sample_product_data)
        
        response = client.get("/products")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
    
    def test_get_product_by_id(self, client, sample_product_data):
        """Prueba obtener producto por ID"""
        # Crear producto
        create_response = client.post("/products", json=sample_product_data)
        product_id = create_response.json()["product_id"]
        
        # Obtener producto
        response = client.get(f"/products/{product_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == sample_product_data["name"]
        assert data["price"] == sample_product_data["price"]
    
    def test_get_product_not_found(self, client):
        """Prueba obtener producto que no existe"""
        response = client.get("/products/nonexistent")
        assert response.status_code == 404
        assert "Product not found" in response.json()["detail"]
    
    def test_update_product(self, client, sample_product_data):
        """Prueba actualizar producto"""
        # Crear producto
        create_response = client.post("/products", json=sample_product_data)
        product_id = create_response.json()["product_id"]
        
        # Actualizar producto
        update_data = {"name": "Producto Actualizado", "price": 1500.00}
        response = client.put(f"/products/{product_id}", json=update_data)
        assert response.status_code == 200
        
        # Verificar actualización
        get_response = client.get(f"/products/{product_id}")
        assert get_response.json()["name"] == "Producto Actualizado"
        assert get_response.json()["price"] == 1500.00
    
    def test_update_product_not_found(self, client):
        """Prueba actualizar producto que no existe"""
        response = client.put("/products/nonexistent", json={"name": "Test"})
        assert response.status_code == 404
    
    def test_delete_product(self, client, sample_product_data):
        """Prueba eliminar producto"""
        # Crear producto
        create_response = client.post("/products", json=sample_product_data)
        product_id = create_response.json()["product_id"]
        
        # Eliminar producto
        response = client.delete(f"/products/{product_id}")
        assert response.status_code == 200
        
        # Verificar eliminación
        get_response = client.get(f"/products/{product_id}")
        assert get_response.status_code == 404
    
    def test_delete_product_with_sales(self, client, setup_test_data):
        """Prueba que no se pueda eliminar producto con ventas"""
        client_id = setup_test_data["client_id"]
        product_id = setup_test_data["product_id"]
        
        # Crear venta
        client.post("/sales", json={
            "client_id": client_id,
            "product_id": product_id,
            "quantity": 1
        })
        
        # Intentar eliminar producto
        response = client.delete(f"/products/{product_id}")
        assert response.status_code == 400
        assert "Cannot delete product with existing sales" in response.json()["detail"]
