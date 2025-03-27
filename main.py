from db.modelos import Clientes, Productos
from app.clientes.registrar import registrar as registrarNuevoCliente
from app.productos.registrar import registrar as registrarNuevoProducto
from app.pedidos.registrar import PedidoARegistrar, registrar as registrarNuevoPedido
from app.clientes.consultar_pedidos import actualizar_estado_pedido, consultarPedidos
from app import app
from fastapi import FastAPI, HTTPException
from app.clientes.consultar_pedidos import consultar_estado_pedido
from pydantic import BaseModel

@app.get("/api/v1/ok")
def read_root():
    return {"status": "ok"}

@app.post("/api/v1/cliente")
def post_cliente(cliente: Clientes):
    return registrarNuevoCliente(cliente)

@app.post("/api/v1/productos")
def post_productos(producto: Productos):
    return registrarNuevoProducto(producto)

@app.post("/api/v1/pedidos")
def post_pedidos(pedido: PedidoARegistrar):
    return registrarNuevoPedido(pedido)

@app.get("/api/v1/clientes/{cliente_id}/pedidos")
def get_pedidos_de_un_cliente(cliente_id: str):
    pedidos = consultarPedidos(cliente_id)
    return{"pedidos": pedidos}

@app.get("/api/v1/pedidos/{pedido_id}/estado")
def get_estado_del_pedido(pedido_id: str):
    estado = consultar_estado_pedido(pedido_id)
    
    if estado is None:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    
    return {"pedido_id": pedido_id, "estado": estado.estado}



from datetime import datetime

# Modelo Pydantic para los pedidos, que solo incluye los campos que necesitas.
class PedidoResponse(BaseModel):
    order_id: str
    status: str
    created_at: datetime

    class Config:
        # Permite que el modelo Pydantic pueda convertir instancias de SQLModel a JSON.
        orm_mode = True
        
@app.get("/api/v1/clientes/{cliente_id}/pedidos", response_model=list[PedidoResponse])
def get_pedidos_de_un_cliente(cliente_id: str):
    pedidos = consultarPedidos(cliente_id)
    if not pedidos:
        raise HTTPException(status_code=404, detail="No se encontraron pedidos para este cliente.")
    
    # Convertimos los objetos Pedidos a los modelos Pydantic
    pedidos_response = [PedidoResponse(order_id=pedido.id, status=pedido.estado, created_at=pedido.created_at) for pedido in pedidos]
    
    return {"pedidos": pedidos_response}



# Definir el modelo de entrada para el estado
class EstadoPedido(BaseModel):
    estado: str

@app.put("/api/v1/pedidos/{pedido_id}/estado")
def put_estado_pedido(pedido_id: str, estado_pedido: EstadoPedido):
    # Actualizamos el estado del pedido con la función correspondiente
    resultado = actualizar_estado_pedido(pedido_id, estado_pedido.estado)
    
    if not resultado:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    
    # Obtener el pedido actualizado para devolver la respuesta con la nueva información
    pedido_actualizado = consultar_estado_pedido(pedido_id)
    
    return {
        "order_id": pedido_actualizado.id,
        "status": pedido_actualizado.estado,
        "updated_at": pedido_actualizado.updated_at.isoformat()
    }