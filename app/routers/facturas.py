from fastapi import APIRouter, HTTPException, status
from app.models.factura import Factura
from app.database import lista_clientes, lista_facturas

router = APIRouter(prefix="/facturas", tags=["Facturas"])

@router.get("/", response_model=list[Factura])
async def mostrar_facturas():
    return lista_facturas

@router.post("/", response_model=Factura, status_code=status.HTTP_201_CREATED)
async def guardar_factura(datos: Factura):
    for factura in lista_facturas:
        if factura.id == datos.id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El ID de la factura ya existe")

    cliente_existe = False
    for cliente in lista_clientes:
        if cliente.nombre == datos.cliente:
            cliente_existe = True
            break

    if not cliente_existe:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"No se puede crear la factura. El cliente '{datos.cliente}' no existe."
        )

    lista_facturas.append(datos)
    return datos