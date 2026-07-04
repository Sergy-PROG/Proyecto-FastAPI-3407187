from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

# 1. Esquemas Base
class ClienteBase(SQLModel):
    nombre: str = Field(default=None)
    email: str = Field(default=None)
    descripcion: Optional[str] = Field(default=None)

class ClienteCrear(ClienteBase):
    pass  

class ClienteEditar(ClienteBase):
    pass  

# 2. El modelo de la Tabla Física
class Cliente(ClienteBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # SOLUCIÓN DEFINITIVA: Usamos el tipado nativo de List y apuntamos al nombre del modelo en string limpio
    facturas: List["Factura"] = Relationship(back_populates="cliente")

# 3. Esquema de Respuesta Virtual
class ClienteConFacturas(ClienteBase):
    id: int
    facturas: List["FacturaPublica"] = []

# Importaciones al final para evitar importación circular
from modelos.facturas import Factura, FacturaPublica