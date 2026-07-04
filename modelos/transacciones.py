from typing import Optional
from sqlmodel import SQLModel, Field, Relationship

# 1. Esquema Base
class TransaccionBase(SQLModel):
    concepto: str = Field(default=None)
    monto: float = Field(default=None)
    factura_id: int = Field(foreign_key="factura.id")

# --- ESTA ES LA CLASE QUE HACÍA FALTA ---
class TransaccionCrear(TransaccionBase):
    pass  # Hereda todos los campos obligatorios para la creación
# ----------------------------------------

class TransaccionEditar(SQLModel):
    concepto: Optional[str] = None
    monto: Optional[float] = None
    factura_id: Optional[int] = None

# 2. Modelo de Tabla Física
class Transaccion(TransaccionBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    
    factura: Optional["Factura"] = Relationship(back_populates="transacciones")

# 3. Esquema de Respuesta Virtual
class TransaccionPublica(TransaccionBase):
    id: int

# Importación al final para evitar bucles circulares
from modelos.facturas import Factura