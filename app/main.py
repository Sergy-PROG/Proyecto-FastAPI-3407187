from fastapi import FastAPI
from app.routers import clientes, facturas, transacciones

app = FastAPI(
    title="Sistema de Facturación Modular",
    description="Proyecto estructurado profesionalmente siguiendo las pautas de clase",
    version="2.0.0"
)

app.include_router(clientes.router)
app.include_router(facturas.router)
app.include_router(transacciones.router)