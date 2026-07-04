from fastapi import APIRouter, HTTPException, status
# Asegúrate de importar FacturaCrear
from modelos.facturas import Factura, FacturaEditar, FacturaConDetalles, FacturaPublica, FacturaCrear
from base_de_datos import SesionDependencia
from sqlmodel import select
from modelos.clientes import Cliente  

router = APIRouter(prefix="/facturas", tags=["Facturas"])

@router.get("", response_model=list[FacturaPublica])
async def listar_facturas(mi_sesion: SesionDependencia):
    lista_facturas = mi_sesion.exec(select(Factura)).all()
    return lista_facturas

@router.get("/{factura_id}", response_model=FacturaConDetalles)
async def consultar_factura(factura_id: int, mi_sesion: SesionDependencia):
    factura_bd = mi_sesion.get(Factura, factura_id)
    if not factura_bd:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"La factura con ID {factura_id} no existe."
        )
    return factura_bd 

@router.post("", response_model=FacturaPublica)
async def crear_factura(datos_factura: FacturaCrear, mi_sesion: SesionDependencia): # <-- Cambiado a FacturaCrear
    cliente_existente = mi_sesion.get(Cliente, datos_factura.cliente_id)
    if not cliente_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No se puede crear la factura. El cliente con ID {datos_factura.cliente_id} no existe."
        )
    
    # Pydantic procesa el string de la fecha JSON y lo convierte a un datetime de Python real
    nueva_factura_dict = datos_factura.model_dump()
    factura_validada = Factura(**nueva_factura_dict)
    
    mi_sesion.add(factura_validada)
    mi_sesion.commit()
    mi_sesion.refresh(factura_validada)
    
    return factura_validada

@router.put("/{id}", response_model=FacturaPublica)
async def editar_factura(id: int, datos_actualizados: FacturaEditar, mi_sesion: SesionDependencia): 
    factura_bd = mi_sesion.get(Factura, id)
    if not factura_bd:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"La factura con ID {id} no existe."
        )
    
    datos_dict = datos_actualizados.model_dump(exclude_unset=True)
    factura_bd.sqlmodel_update(datos_dict)
    
    mi_sesion.add(factura_bd)
    mi_sesion.commit()
    mi_sesion.refresh(factura_bd)
    return factura_bd

@router.delete("/{id}")
async def eliminar_factura(id: int, mi_sesion: SesionDependencia):
    factura_bd = mi_sesion.get(Factura, id)
    if not factura_bd:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"La factura con ID {id} no existe."
        )
    
    mi_sesion.delete(factura_bd)
    mi_sesion.commit()
    return {"mensaje": "La factura fue eliminada con éxito"}