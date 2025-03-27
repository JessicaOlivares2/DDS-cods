from sqlmodel import SQLModel
from db.conexion import db

def crearBDDYSusTablas():
    SQLModel.metadata.create_all(db)