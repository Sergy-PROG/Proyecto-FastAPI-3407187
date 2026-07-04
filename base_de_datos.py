from typing import Annotated
from fastapi import FastAPI, Depends
from sqlmodel import SQLModel, create_engine, Session

nombre_bd = "clientes.sqlite3"
url_bd = f"sqlite:///{nombre_bd}"

motor_bd = create_engine(url_bd)

def crear_tablas(app: FastAPI):
    SQLModel.metadata.create_all(motor_bd)
    yield

def obtener_sesion():
    with Session(motor_bd) as mi_sesion:
        yield mi_sesion

SesionDependencia = Annotated[Session, Depends(obtener_sesion)]