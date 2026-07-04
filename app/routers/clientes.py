from fastapi import APIRouter, HTTPException, status
from app.models.cliente import Cliente
from app.database import lista_clientes

router = APIRouter(prefix="/clientes", tags=["Clientes"])

@router.get("/", response_model=list[Cliente])
async def mostrar_clientes():
    return lista_clientes

@router.get("/{id}", response_model=Cliente)
async def buscar_un_cliente(id: int):
    for cliente in lista_clientes:
        if cliente.id == id:
            return cliente
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se encontró el cliente")

@router.post("/", response_model=Cliente, status_code=status.HTTP_201_CREATED)
async def guardar_cliente(datos: Cliente):
    for cliente in lista_clientes:
        if cliente.id == datos.id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El ID del cliente ya existe")
    lista_clientes.append(datos)
    return datos