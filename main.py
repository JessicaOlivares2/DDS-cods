from db.modelos import Clientes, Productos
from app.clientes.registrar import registrar as registrarNuevoCliente
from app.productos.registrar import registrar as registrarNuevoProducto
from app.pedidos.registrar import PedidoARegistrar, registrar as registrarNuevoPedido
from app.clientes.consultar_pedidos import consultarPedidos
from app import app
from fastapi import FastAPI, HTTPException
from app.clientes.consultar_pedidos import consultar_estado_pedido


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
    
    return {"pedido_id": pedido_id, "estado": estado}


