from pydantic import BaseModel

class Factura(BaseModel):
    id: int
    fecha: str
    valor_total: float
    cliente: str