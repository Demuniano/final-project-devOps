# Store API - Backend FastAPI

API REST para gestión de clientes, productos y ventas con métricas de Prometheus.

## Características

- **CRUD completo** para Clientes, Productos y Ventas
- **Métricas de Prometheus** en `/metrics`
- **Documentación automática** con Swagger/OpenAPI
- **Validaciones robustas** y manejo de errores
- **Pruebas unitarias e integración** con pytest
- **Health check** en `/health`

## Instalación y Ejecución Local

### Prerrequisitos

- Python 3.8+
- pip

### Pasos

1. **Clonar el repositorio**
   ```bash
   git clone <repo-url>
   cd final-project-devOps
   ```

2. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

3. **Ejecutar la aplicación**
   ```bash
   python run.py
   ```

4. **Acceder a la API**
   - API: http://localhost:5000
   - Documentación: http://localhost:5000/docs
   - Métricas: http://localhost:5000/metrics
   - Health: http://localhost:5000/health

## Endpoints Principales

### Clientes

- `POST /clients` - Crear cliente
- `GET /clients` - Listar todos los clientes
- `GET /clients/{id}` - Obtener cliente específico
- `PUT /clients/{id}` - Actualizar cliente
- `DELETE /clients/{id}` - Eliminar cliente

### Productos

- `POST /products` - Crear producto
- `GET /products` - Listar todos los productos
- `GET /products/{id}` - Obtener producto específico
- `PUT /products/{id}` - Actualizar producto
- `DELETE /products/{id}` - Eliminar producto

### Ventas

- `POST /sales` - Crear venta
- `GET /sales` - Listar todas las ventas
- `GET /sales/{id}` - Obtener venta específica
- `GET /sales/client/{client_id}` - Ventas por cliente
- `GET /sales/product/{product_id}` - Ventas por producto

## Ejemplos de Uso

### Crear Cliente

```bash
curl -X POST "http://localhost:5000/clients" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Juan Pérez",
    "email": "juan@email.com",
    "phone": "+1234567890"
  }'
```

**Respuesta:**
```json
{
  "message": "Client created successfully",
  "client_id": "123e4567-e89b-12d3-a456-426614174000"
}
```

### Crear Producto

```bash
curl -X POST "http://localhost:5000/products" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Laptop Gaming",
    "price": 1299.99,
    "description": "Laptop para gaming de alta gama",
    "stock": 10
  }'
```

### Crear Venta

```bash
curl -X POST "http://localhost:5000/sales" \
  -H "Content-Type: application/json" \
  -d '{
    "client_id": "123e4567-e89b-12d3-a456-426614174000",
    "product_id": "987fcdeb-51f2-4321-b098-765432109876",
    "quantity": 2
  }'
```

## Pruebas

### Ejecutar todas las pruebas

```bash
pytest
```

### Ejecutar pruebas con cobertura

```bash
pytest --cov=app tests/
```

### Ejecutar pruebas específicas

```bash
# Solo pruebas de clientes
pytest tests/test_clients.py

# Solo pruebas de productos
pytest tests/test_products.py

# Solo pruebas de ventas
pytest tests/test_sales.py

# Solo pruebas de integración
pytest tests/test_integration.py
```

## Métricas de Prometheus

La API expone las siguientes métricas en `/metrics`:

- `http_requests_total` - Total de requests HTTP por método, endpoint y status code
- `http_request_duration_seconds` - Latencia de requests por endpoint
- `http_errors_total` - Total de errores HTTP por tipo
- `active_clients_total` - Número total de clientes activos
- `active_products_total` - Número total de productos activos
- `sales_total` - Número total de ventas
- `revenue_total` - Revenue total de todas las ventas

### Configurar Prometheus

Agregar a `prometheus.yml`:

```yaml
scrape_configs:
  - job_name: 'store-api'
    static_configs:
      - targets: ['localhost:5000']
    metrics_path: '/metrics'
    scrape_interval: 15s
```

## Estructura del Proyecto

```
final-project-devOps/
├── app/
│   ├── __init__.py          # Configuración principal de FastAPI
│   ├── routes.py            # Endpoints CRUD
│   └── metrics.py           # Configuración de métricas Prometheus
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Fixtures compartidas
│   ├── test_clients.py      # Pruebas de clientes
│   ├── test_products.py     # Pruebas de productos
│   ├── test_sales.py        # Pruebas de ventas
│   └── test_integration.py  # Pruebas de integración
├── requirements.txt         # Dependencias
├── run.py                   # Punto de entrada
└── README.md               # Esta documentación
```

## Contribuir

### Estándares de Código

- Seguir PEP8
- Usar type hints
- Documentar funciones con docstrings
- Mantener cobertura de pruebas >90%

### Proceso de Desarrollo

1. Crear rama feature desde `develop`
2. Implementar cambios con pruebas
3. Ejecutar pruebas localmente
4. Crear Pull Request a `develop`
5. Code review
6. Merge tras aprobación

### Formato de Código

```bash
# Formatear código con black
black app/ tests/

# Verificar imports con isort
isort app/ tests/

# Verificar linting con flake8
flake8 app/ tests/
```

## CI/CD

Las pruebas se ejecutan automáticamente en:
- Cada push a `develop`
- Cada Pull Request
- Cada merge a `main`

## Monitoreo

- **Health Check**: `/health`
- **Métricas**: `/metrics` (compatible con Prometheus)
- **Logs**: Estructurados con uvicorn

## Soporte

Para dudas o contribuciones, contactar al equipo de desarrollo o crear un issue en el repositorio.
