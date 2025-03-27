from datetime import datetime
from sqlmodel import Field, SQLModel
from uuid import uuid4

class Clientes(SQLModel, table=True):
    id: str = Field(default=str(uuid4()), primary_key=True)
    created_at: datetime = Field(default=datetime.now())
    updated_at: datetime = Field(default_factory=datetime.now)
    nombre: str
    apellido: str

class Pedidos(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    cliente_id: str
    estado: str = Field(default="pendiente")

class Productos(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    descripcion: str

class ProductosEnPedidos(SQLModel, table=True):
    id: str = Field(default=str(uuid4()), primary_key=True)
    created_at: datetime = Field(default=datetime.now())
    updated_at: datetime = Field(default_factory=datetime.now)
    pedido_id: str = Field(foreign_key="pedidos.id")
    producto_id: str = Field(foreign_key="productos.id")
    cantidad: int