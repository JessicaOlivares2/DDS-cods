from datetime import datetime
from sqlmodel import Session, select, update 
from db.conexion import db
from db.modelos import Pedidos

def consultarPedidos(cliente_id: str):
    with Session(db) as sesion:
        consulta = select(Pedidos).where(Pedidos.cliente_id == cliente_id)
        pedidos = sesion.exec(consulta).all()  # Usar .all() para obtener todos los resultados
        return pedidos  # Devolvemos la lista de objetos Pedidos

    
def consultar_estado_pedido(pedido_id: str):
    with Session(db) as sesion:
        consulta = select(Pedidos).where(Pedidos.id == pedido_id)
        pedido = sesion.exec(consulta).first()  
        
        if pedido is None:
            return None  # No se encontró el pedido
        
        return pedido


def actualizar_estado_pedido(pedido_id: str, nuevo_estado: str) -> bool:
    with Session(db) as session:
        # Buscar el pedido con el ID proporcionado
        pedido = session.exec(select(Pedidos).where(Pedidos.id == pedido_id)).first()
        
        if not pedido:
            return False  # No se encontró el pedido
        
        # Actualizar el estado del pedido
        pedido.estado = nuevo_estado
        pedido.updated_at = datetime.now()  # Actualizamos la fecha de modificación
        session.add(pedido)  # Añadimos el pedido actualizado
        session.commit()  # Guardamos los cambios
        
        return True  