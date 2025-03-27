from contextlib import asynccontextmanager
from fastapi import FastAPI
from db.inicializar import crearBDDYSusTablas

@asynccontextmanager
async def cicloDeVidaDeLaAPP(app: FastAPI):
    print("Inicio de la app")
    crearBDDYSusTablas()
    yield
    print("Fin de la app")

app = FastAPI(lifespan=cicloDeVidaDeLaAPP)