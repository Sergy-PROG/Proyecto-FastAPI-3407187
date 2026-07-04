from typing import Optional, List
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship

# 1. Esquema Base
class FacturaBase(SQLModel):
    fecha: datetime = Field(default_factory=datetime.now)
    valor_total: float = Field(default=0.0)
    cliente_id: int = Field(foreign_key="cliente.id")

class FacturaCrear(FacturaBase):
    pass

class FacturaEditar(SQLModel):
    fecha: Optional[datetime] = None
    valor_total: Optional[float] = None
    cliente_id: Optional[int] = None

# 2. Modelo de Tabla Física
class Factura(FacturaBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    
    cliente: Optional["Cliente"] = Relationship(back_populates="facturas")
    # SOLUCIÓN DEFINITIVA: Transacciones usando la clase en un string limpio sin List dentro del string
    transacciones: List["Transaccion"] = Relationship(back_populates="factura")

# 3. Esquemas de Respuesta Virtuales
class FacturaPublica(FacturaBase):
    id: int

class FacturaConDetalles(FacturaBase):
    id: int
    cliente: Optional["ClienteBase"] = None
    transacciones: List["TransaccionPublica"] = []

from modelos.clientes import Cliente, ClienteBase
from modelos.transacciones import Transaccion, TransaccionPublica