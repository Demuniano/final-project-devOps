from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Optional
from uuid import uuid4
from datetime import datetime

router = APIRouter()

# In-memory storage
clients = {}
products = {}
sales = []

# Pydantic models
class ClientIn(BaseModel):
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None

class ClientOut(BaseModel):
    id: str
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    created_at: datetime

class ClientUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None

class ProductIn(BaseModel):
    name: str
    price: float
    description: Optional[str] = None
    stock: int = 0

class ProductOut(BaseModel):
    id: str
    name: str
    price: float
    description: Optional[str] = None
    stock: int
    created_at: datetime

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None
    stock: Optional[int] = None

class SaleIn(BaseModel):
    client_id: str
    product_id: str
    quantity: int

class SaleOut(BaseModel):
    id: str
    client_id: str
    product_id: str
    quantity: int
    total_amount: float
    created_at: datetime

# CLIENTS ENDPOINTS
@router.post("/clients", response_model=Dict[str, str])
def create_client(client: ClientIn):
    """Crear un nuevo cliente"""
    if not client.name.strip():
        raise HTTPException(status_code=400, detail="Client name cannot be empty")
    
    client_id = str(uuid4())
    clients[client_id] = {
        "id": client_id, 
        "name": client.name,
        "email": client.email,
        "phone": client.phone,
        "created_at": datetime.now()
    }
    return {"message": "Client created successfully", "client_id": client_id}

@router.get("/clients", response_model=List[ClientOut])
def get_clients():
    """Obtener todos los clientes"""
    return list(clients.values())

@router.get("/clients/{client_id}", response_model=ClientOut)
def get_client(client_id: str):
    """Obtener un cliente específico por ID"""
    if client_id not in clients:
        raise HTTPException(status_code=404, detail="Client not found")
    return clients[client_id]

@router.put("/clients/{client_id}", response_model=Dict[str, str])
def update_client(client_id: str, client_update: ClientUpdate):
    """Actualizar un cliente existente"""
    if client_id not in clients:
        raise HTTPException(status_code=404, detail="Client not found")
    
    client = clients[client_id]
    update_data = client_update.model_dump(exclude_unset=True)
    
    if "name" in update_data and not update_data["name"].strip():
        raise HTTPException(status_code=400, detail="Client name cannot be empty")
    
    client.update(update_data)
    return {"message": "Client updated successfully"}

@router.delete("/clients/{client_id}", response_model=Dict[str, str])
def delete_client(client_id: str):
    """Eliminar un cliente"""
    if client_id not in clients:
        raise HTTPException(status_code=404, detail="Client not found")
    
    # Check if client has sales
    client_sales = [sale for sale in sales if sale.get("client_id") == client_id]
    if client_sales:
        raise HTTPException(status_code=400, detail="Cannot delete client with existing sales")
    
    del clients[client_id]
    return {"message": "Client deleted successfully"}

# PRODUCTS ENDPOINTS
@router.post("/products", response_model=Dict[str, str])
def create_product(product: ProductIn):
    """Crear un nuevo producto"""
    if not product.name.strip():
        raise HTTPException(status_code=400, detail="Product name cannot be empty")
    if product.price <= 0:
        raise HTTPException(status_code=400, detail="Product price must be greater than 0")
    
    product_id = str(uuid4())
    products[product_id] = {
        "id": product_id,
        "name": product.name,
        "price": product.price,
        "description": product.description,
        "stock": product.stock,
        "created_at": datetime.now()
    }
    return {"message": "Product created successfully", "product_id": product_id}

@router.get("/products", response_model=List[ProductOut])
def get_products():
    """Obtener todos los productos"""
    return list(products.values())

@router.get("/products/{product_id}", response_model=ProductOut)
def get_product(product_id: str):
    """Obtener un producto específico por ID"""
    if product_id not in products:
        raise HTTPException(status_code=404, detail="Product not found")
    return products[product_id]

@router.put("/products/{product_id}", response_model=Dict[str, str])
def update_product(product_id: str, product_update: ProductUpdate):
    """Actualizar un producto existente"""
    if product_id not in products:
        raise HTTPException(status_code=404, detail="Product not found")
    
    product = products[product_id]
    update_data = product_update.model_dump(exclude_unset=True)
    
    if "name" in update_data and not update_data["name"].strip():
        raise HTTPException(status_code=400, detail="Product name cannot be empty")
    if "price" in update_data and update_data["price"] <= 0:
        raise HTTPException(status_code=400, detail="Product price must be greater than 0")
    
    product.update(update_data)
    return {"message": "Product updated successfully"}

@router.delete("/products/{product_id}", response_model=Dict[str, str])
def delete_product(product_id: str):
    """Eliminar un producto"""
    if product_id not in products:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Check if product has sales
    product_sales = [sale for sale in sales if sale.get("product_id") == product_id]
    if product_sales:
        raise HTTPException(status_code=400, detail="Cannot delete product with existing sales")
    
    del products[product_id]
    return {"message": "Product deleted successfully"}

# SALES ENDPOINTS
@router.post("/sales")
def create_sale(sale: SaleIn):
    """Crear una nueva venta"""
    if sale.client_id not in clients:
        raise HTTPException(status_code=400, detail="Client not found")
    if sale.product_id not in products:
        raise HTTPException(status_code=400, detail="Product not found")
    if sale.quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be greater than 0")
    
    product = products[sale.product_id]
    if product["stock"] < sale.quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock")
    
    sale_id = str(uuid4())
    total_amount = product["price"] * sale.quantity
    
    sale_record = {
        "id": sale_id,
        "client_id": sale.client_id,
        "product_id": sale.product_id,
        "quantity": sale.quantity,
        "total_amount": total_amount,
        "created_at": datetime.now()
    }
    
    sales.append(sale_record)
    # Update product stock
    products[sale.product_id]["stock"] -= sale.quantity
    
    return {"message": "Sale created successfully", "sale_id": sale_id, "total_amount": f"{total_amount:.2f}"}

@router.get("/sales", response_model=List[SaleOut])
def get_sales():
    """Obtener todas las ventas"""
    return sales

@router.get("/sales/{sale_id}", response_model=SaleOut)
def get_sale(sale_id: str):
    """Obtener una venta específica por ID"""
    sale = next((s for s in sales if s["id"] == sale_id), None)
    if not sale:
        raise HTTPException(status_code=404, detail="Sale not found")
    return sale

@router.get("/sales/client/{client_id}", response_model=List[SaleOut])
def get_sales_by_client(client_id: str):
    """Obtener todas las ventas de un cliente específico"""
    if client_id not in clients:
        raise HTTPException(status_code=404, detail="Client not found")
    client_sales = [sale for sale in sales if sale["client_id"] == client_id]
    return client_sales

@router.get("/sales/product/{product_id}", response_model=List[SaleOut])
def get_sales_by_product(product_id: str):
    """Obtener todas las ventas de un producto específico"""
    if product_id not in products:
        raise HTTPException(status_code=404, detail="Product not found")
    product_sales = [sale for sale in sales if sale["product_id"] == product_id]
    return product_sales
