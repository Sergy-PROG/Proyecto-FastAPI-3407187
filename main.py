from fastapi import FastAPI
from enrutadores import clientes, facturas, transacciones 
from base_de_datos import crear_tablas

app = FastAPI(
    title="Sistema de Facturación Modular",
    description="Aprendiendo a usar el APIRouter",
    lifespan=crear_tablas 
)

app.include_router(clientes.router)
app.include_router(facturas.router)
app.include_router(transacciones.router)

@app.get("/")
async def inicio():
    return {"mensaje": "Bienvenido a la API de Facturación"}