from fastapi import APIRouter, HTTPException, status
# Importamos TransaccionCrear y TransaccionPublica
from modelos.transacciones import Transaccion, TransaccionEditar, TransaccionCrear, TransaccionPublica
from base_de_datos import SesionDependencia
from sqlmodel import select
from modelos.facturas import Factura  

router = APIRouter(prefix="/transacciones", tags=["Transacciones"])

@router.get("", response_model=list[TransaccionPublica])
async def listar_transacciones(mi_sesion: SesionDependencia):
    lista_transacciones = mi_sesion.exec(select(Transaccion)).all()
    return lista_transacciones

@router.get("/{id}", response_model=TransaccionPublica)
async def consultar_transaccion(id: int, mi_sesion: SesionDependencia):
    transaccion_bd = mi_sesion.get(Transaccion, id)
    if not transaccion_bd:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"La transacción con ID {id} no existe."
        )
    return transaccion_bd

@router.post("", response_model=TransaccionPublica)
async def crear_transaccion(datos_transaccion: TransaccionCrear, mi_sesion: SesionDependencia):
    # 1. Validamos si la factura existe antes de proceder
    factura_existente = mi_sesion.get(Factura, datos_transaccion.factura_id)
    if not factura_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No se puede crear la transacción. La factura con ID {datos_transaccion.factura_id} no existe."
        )
    
    # 2. Convertimos el esquema de entrada a un diccionario e instanciamos el modelo físico
    nueva_transaccion_dict = datos_transaccion.model_dump()
    transaccion_validada = Transaccion(**nueva_transaccion_dict)
    
    mi_sesion.add(transaccion_validada)
    mi_sesion.commit()
    mi_sesion.refresh(transaccion_validada)
    
    return transaccion_validada

@router.put("/{id}", response_model=TransaccionPublica)
async def editar_transaccion(id: int, datos_actualizados: TransaccionEditar, mi_sesion: SesionDependencia): 
    transaccion_bd = mi_sesion.get(Transaccion, id)
    if not transaccion_bd:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"La transacción con ID {id} no existe."
        )
    
    datos_dict = datos_actualizados.model_dump(exclude_unset=True)
    transaccion_bd.sqlmodel_update(datos_dict)
    
    mi_sesion.add(transaccion_bd)
    mi_sesion.commit()
    mi_sesion.refresh(transaccion_bd)
    return transaccion_bd

@router.delete("/{id}")
async def eliminar_transaccion(id: int, mi_sesion: SesionDependencia):
    transaccion_bd = mi_sesion.get(Transaccion, id)
    if not transaccion_bd:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"La transacción con ID {id} no existe."
        )
    
    mi_sesion.delete(transaccion_bd)
    mi_sesion.commit()
    return {"mensaje": "La transacción fue eliminada con éxito"}