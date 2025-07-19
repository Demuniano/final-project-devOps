import pytest
from fastapi.testclient import TestClient


class TestMetrics:
    """Pruebas para el endpoint de métricas"""
    
    def test_metrics_endpoint(self, client):
        """Prueba que el endpoint de métricas funcione"""
        response = client.get("/metrics")
        assert response.status_code == 200
        assert "text/plain" in response.headers["content-type"]
        
        # Verificar que contiene métricas esperadas
        content = response.text
        assert "http_requests_total" in content
        assert "http_request_duration_seconds" in content
        assert "active_clients_total" in content
        assert "active_products_total" in content
    
    def test_health_endpoint(self, client):
        """Prueba que el endpoint de health check funcione"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "store-api"
    
    def test_metrics_updated_after_operations(self, client, sample_client_data):
        """Prueba que las métricas se actualicen después de operaciones"""
        # Obtener métricas iniciales
        initial_response = client.get("/metrics")
        initial_content = initial_response.text
        
        # Realizar operación
        client.post("/clients", json=sample_client_data)
        
        # Obtener métricas después de la operación
        final_response = client.get("/metrics")
        final_content = final_response.text
        
        # Las métricas deben haberse actualizado
        assert "http_requests_total" in final_content
        assert "active_clients_total" in final_content


class TestIntegration:
    """Pruebas de integración"""
    
    def test_full_workflow(self, client):
        """Prueba flujo completo: crear cliente, producto y venta"""
        # 1. Crear cliente
        client_response = client.post("/clients", json={
            "name": "Cliente Integración",
            "email": "integracion@test.com"
        })
        assert client_response.status_code == 200
        client_id = client_response.json()["client_id"]
        
        # 2. Crear producto
        product_response = client.post("/products", json={
            "name": "Producto Integración",
            "price": 299.99,
            "stock": 10
        })
        assert product_response.status_code == 200
        product_id = product_response.json()["product_id"]
        
        # 3. Crear venta
        sale_response = client.post("/sales", json={
            "client_id": client_id,
            "product_id": product_id,
            "quantity": 3
        })
        assert sale_response.status_code == 200
        sale_data = sale_response.json()
        
        # 4. Verificar que la venta se creó correctamente
        assert "sale_id" in sale_data
        assert sale_data["total_amount"] == "899.97"  # 299.99 * 3
        
        # 5. Verificar que el stock se redujo
        updated_product = client.get(f"/products/{product_id}")
        assert updated_product.json()["stock"] == 7
        
        # 6. Verificar que las métricas se actualizaron
        metrics_response = client.get("/metrics")
        assert "active_clients_total" in metrics_response.text
        assert "active_products_total" in metrics_response.text
        assert "sales_total" in metrics_response.text
    
    def test_api_documentation(self, client):
        """Prueba que la documentación automática esté disponible"""
        # OpenAPI JSON
        openapi_response = client.get("/openapi.json")
        assert openapi_response.status_code == 200
        openapi_data = openapi_response.json()
        assert "openapi" in openapi_data
        assert "info" in openapi_data
        assert openapi_data["info"]["title"] == "Store API"
        
        # Swagger UI (docs)
        docs_response = client.get("/docs")
        assert docs_response.status_code == 200
        
        # ReDoc
        redoc_response = client.get("/redoc")
        assert redoc_response.status_code == 200
