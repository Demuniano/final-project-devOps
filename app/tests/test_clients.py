import pytest
from fastapi.testclient import TestClient


class TestClients:
    """Pruebas para endpoints de clientes"""
    
    def test_create_client_success(self, client, sample_client_data):
        """Prueba crear cliente exitosamente"""
        response = client.post("/clients", json=sample_client_data)
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Client created successfully"
        assert "client_id" in data
    
    def test_create_client_empty_name(self, client):
        """Prueba crear cliente con nombre vacío"""
        response = client.post("/clients", json={"name": ""})
        assert response.status_code == 400
        assert "Client name cannot be empty" in response.json()["detail"]
    
    def test_get_clients(self, client, sample_client_data):
        """Prueba obtener lista de clientes"""
        # Crear un cliente primero
        client.post("/clients", json=sample_client_data)
        
        response = client.get("/clients")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
    
    def test_get_client_by_id(self, client, sample_client_data):
        """Prueba obtener cliente por ID"""
        # Crear cliente
        create_response = client.post("/clients", json=sample_client_data)
        client_id = create_response.json()["client_id"]
        
        # Obtener cliente
        response = client.get(f"/clients/{client_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == sample_client_data["name"]
        assert data["email"] == sample_client_data["email"]
    
    def test_get_client_not_found(self, client):
        """Prueba obtener cliente que no existe"""
        response = client.get("/clients/nonexistent")
        assert response.status_code == 404
        assert "Client not found" in response.json()["detail"]
    
    def test_update_client(self, client, sample_client_data):
        """Prueba actualizar cliente"""
        # Crear cliente
        create_response = client.post("/clients", json=sample_client_data)
        client_id = create_response.json()["client_id"]
        
        # Actualizar cliente
        update_data = {"name": "Nombre Actualizado"}
        response = client.put(f"/clients/{client_id}", json=update_data)
        assert response.status_code == 200
        
        # Verificar actualización
        get_response = client.get(f"/clients/{client_id}")
        assert get_response.json()["name"] == "Nombre Actualizado"
    
    def test_update_client_not_found(self, client):
        """Prueba actualizar cliente que no existe"""
        response = client.put("/clients/nonexistent", json={"name": "Test"})
        assert response.status_code == 404
    
    def test_delete_client(self, client, sample_client_data):
        """Prueba eliminar cliente"""
        # Crear cliente
        create_response = client.post("/clients", json=sample_client_data)
        client_id = create_response.json()["client_id"]
        
        # Eliminar cliente
        response = client.delete(f"/clients/{client_id}")
        assert response.status_code == 200
        
        # Verificar eliminación
        get_response = client.get(f"/clients/{client_id}")
        assert get_response.status_code == 404
    
    def test_delete_client_with_sales(self, client, setup_test_data):
        """Prueba que no se pueda eliminar cliente con ventas"""
        client_id = setup_test_data["client_id"]
        product_id = setup_test_data["product_id"]
        
        # Crear venta
        client.post("/sales", json={
            "client_id": client_id,
            "product_id": product_id,
            "quantity": 1
        })
        
        # Intentar eliminar cliente
        response = client.delete(f"/clients/{client_id}")
        assert response.status_code == 400
        assert "Cannot delete client with existing sales" in response.json()["detail"]
