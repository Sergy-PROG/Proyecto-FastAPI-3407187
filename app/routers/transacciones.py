from fastapi import APIRouter, HTTPException, status
from app.models.transaccion import Transaccion
from app.database import lista_facturas, lista_transacciones

router = APIRouter(prefix="/transacciones", tags=["Transacciones"])

@router.get("/", response_model=list[Transaccion])
async def mostrar_transacciones():
    return lista_transacciones

@router.post("/", response_model=Transaccion, status_code=status.HTTP_201_CREATED)
async def guardar_transaccion(datos: Transaccion):
    for transaccion in lista_transacciones:
        if transaccion.id == datos.id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El ID de la transacción ya existe")

    factura_existe = False
    for factura in lista_facturas:
        if factura.id == datos.factura_id:
            factura_existe = True
            break

    if not factura_existe:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"No se puede registrar la transacción. La factura con ID {datos.factura_id} no existe."
        )

    lista_transacciones.append(datos)
    return datos