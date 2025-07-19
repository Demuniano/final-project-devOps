from fastapi import Request
from fastapi.responses import Response
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
import time

# Métricas principales
REQUEST_COUNT = Counter(
    "http_requests_total", 
    "Total HTTP requests", 
    ["method", "endpoint", "status_code"]
)

REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds", 
    "Request latency in seconds", 
    ["endpoint"]
)

REQUEST_ERRORS = Counter(
    "http_errors_total",
    "Total HTTP errors",
    ["method", "endpoint", "error_type"]
)

# Métricas de negocio
ACTIVE_CLIENTS = Gauge("active_clients_total", "Total number of active clients")
ACTIVE_PRODUCTS = Gauge("active_products_total", "Total number of active products")
TOTAL_SALES = Gauge("sales_total", "Total number of sales")
REVENUE_TOTAL = Gauge("revenue_total", "Total revenue from sales")

def update_business_metrics():
    """Actualizar métricas de negocio"""
    from .routes import clients, products, sales
    
    ACTIVE_CLIENTS.set(len(clients))
    ACTIVE_PRODUCTS.set(len(products))
    TOTAL_SALES.set(len(sales))
    
    total_revenue = sum(sale.get("total_amount", 0) for sale in sales)
    REVENUE_TOTAL.set(total_revenue)

def setup_metrics(app):
    @app.middleware("http")
    async def metrics_middleware(request: Request, call_next):
        start_time = time.time()
        
        try:
            response = await call_next(request)
            process_time = time.time() - start_time
            
            # Registrar métricas de request
            REQUEST_LATENCY.labels(endpoint=request.url.path).observe(process_time)
            REQUEST_COUNT.labels(
                method=request.method, 
                endpoint=request.url.path,
                status_code=response.status_code
            ).inc()
            
            # Registrar errores si el status code es >= 400
            if response.status_code >= 400:
                error_type = "client_error" if response.status_code < 500 else "server_error"
                REQUEST_ERRORS.labels(
                    method=request.method,
                    endpoint=request.url.path,
                    error_type=error_type
                ).inc()
            
            # Actualizar métricas de negocio después de operaciones que modifiquen datos
            if request.method in ["POST", "PUT", "DELETE"] and response.status_code < 400:
                update_business_metrics()
            
            return response
            
        except Exception as e:
            process_time = time.time() - start_time
            REQUEST_LATENCY.labels(endpoint=request.url.path).observe(process_time)
            REQUEST_COUNT.labels(
                method=request.method, 
                endpoint=request.url.path,
                status_code=500
            ).inc()
            REQUEST_ERRORS.labels(
                method=request.method,
                endpoint=request.url.path,
                error_type="server_error"
            ).inc()
            raise

    @app.get("/metrics")
    def metrics():
        """Endpoint para exponer métricas de Prometheus"""
        update_business_metrics()  # Actualizar antes de exponer
        return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
    
    @app.get("/health")
    def health_check():
        """Endpoint de health check"""
        return {"status": "healthy", "service": "store-api"}
