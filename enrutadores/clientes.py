from fastapi import APIRouter, HTTPException, status
# Importamos ClienteConFacturas para el GET por ID
from modelos.clientes import Cliente, ClienteCrear, ClienteEditar, ClienteConFacturas
from base_de_datos import SesionDependencia 
from sqlmodel import select 

router = APIRouter(prefix="/clientes", tags=["Clientes"])

@router.get("")
async def listar_clientes(mi_sesion: SesionDependencia):
    lista_clientes = mi_sesion.exec(select(Cliente)).all()
    return {"Clientes": lista_clientes}

# Al agregar response_model=ClienteConFacturas, FastAPI formatea automáticamente el JSON de salida anidado
@router.get("/{cliente_id}", response_model=ClienteConFacturas)
async def listar_cliente(cliente_id: int, mi_sesion: SesionDependencia):
    cliente_bd = mi_sesion.get(Cliente, cliente_id)
    if not cliente_bd:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"El cliente con ID {cliente_id} no existe."
        )
    return cliente_bd # FastAPI leerá la relación virtual de forma automática

@router.post("")
async def crear_clientes(datos_cliente : ClienteCrear, mi_sesion: SesionDependencia):
    nuevo_cliente_dict = datos_cliente.model_dump()
    cliente_validado = Cliente(**nuevo_cliente_dict)
    
    mi_sesion.add(cliente_validado)      
    mi_sesion.commit()                   
    mi_sesion.refresh(cliente_validado)  
    
    return cliente_validado

@router.put("/{id}") 
async def editar_cliente(id: int, datos_actualizados: ClienteEditar, mi_sesion: SesionDependencia):
    cliente_bd = mi_sesion.get(Cliente, id)
    if not cliente_bd:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"El cliente con ID {id} no existe."
        )
    
    cliente_dict = datos_actualizados.model_dump(exclude_unset=True)
    cliente_bd.sqlmodel_update(cliente_dict)
    
    mi_sesion.add(cliente_bd)
    mi_sesion.commit()
    mi_sesion.refresh(cliente_bd)
    
    return cliente_bd

@router.delete("/{id}")
async def eliminar_cliente(id: int, mi_sesion: SesionDependencia):
    # 1. Buscamos el cliente
    cliente_bd = mi_sesion.get(Cliente, id)
    if not cliente_bd:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"El cliente con ID {id} no existe."
        )
    
    # 2. VALIDACIÓN: Verificar si tiene facturas asociadas antes de borrar
    if cliente_bd.facturas:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No se puede eliminar el cliente porque tiene {len(cliente_bd.facturas)} factura(s) asociada(s). Elimina primero sus facturas."
        )
    
    # 3. Si no tiene facturas, lo eliminamos con éxito
    mi_sesion.delete(cliente_bd)
    mi_sesion.commit()
    
    return {"mensaje": "El cliente fue eliminado con éxito"}