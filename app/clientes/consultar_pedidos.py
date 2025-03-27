from sqlmodel import Session, select
from db.conexion import db
from db.modelos import Pedidos

def consultarPedidos(cliente_id: str):
    with Session(db) as sesion:
        consulta = select(Pedidos).where(Pedidos.cliente_id == cliente_id)
        pedidos = sesion.exec(consulta)
        return pedidos
    
def consultar_estado_pedido(pedido_id: str):
    with Session(db) as sesion:
        consulta = select(Pedidos).where(Pedidos.id == pedido_id)
        pedido = sesion.exec(consulta).first()  # Obtiene el primer pedido que coincide con el ID
        
        if pedido is None:
            # Si no se encuentra el pedido, retornar None
            return None
        
        # Si se encuentra el pedido, retornar el estado del pedido
        return pedido.estado