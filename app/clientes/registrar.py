from sqlmodel import Session
from db.modelos import Clientes
from db.conexion import db

def registrar(cliente: Clientes):
    with Session(db) as sesion:
        sesion.add(cliente)
        sesion.commit()
        sesion.refresh(cliente)
    return cliente