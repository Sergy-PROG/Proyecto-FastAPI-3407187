from pydantic import BaseModel

class Transaccion(BaseModel):
    id: int
    vr_unitario: float
    cantidad: int
    factura_id: int