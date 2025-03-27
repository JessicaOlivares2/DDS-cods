from sqlmodel import Session
from db.modelos import Productos
from db.conexion import db

def registrar(producto: Productos):
    with Session(db) as sesion:
        sesion.add(producto)
        sesion.commit()
        sesion.refresh(producto)
    return producto