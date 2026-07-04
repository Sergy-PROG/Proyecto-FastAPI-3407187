from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


# BASES DE DATOS EN MEMORIA (LISTAS)

lista_clientes = []
lista_facturas = []
lista_transacciones = []


# MODELOS DE DATOS (PYDANTIC)

class Cliente(BaseModel):
    id: int
    nombre: str
    descripcion: str | None = None

class Factura(BaseModel):
    id: int
    fecha: str
    valor_total: float
    cliente: str

class Transaccion(BaseModel):
    id: int
    vr_unitario: float
    cantidad: int
    factura_id: int


# MÓDULO 1: CRUD DE CLIENTES

@app.get("/clientes")
def mostrar_clientes():
    return {"Clientes": lista_clientes}

@app.get("/clientes/{id}")
def buscar_un_cliente(id: int):
    for cliente in lista_clientes:
        if cliente.id == id:
            return {"Cliente encontrado": cliente}
    return {"mensaje": "No se encontró el cliente"}

@app.post("/clientes")
def guardar_cliente(datos: Cliente):
    lista_clientes.append(datos)
    return {"mensaje": "Cliente guardado con éxito"}

@app.put("/clientes/{id}")
def modificar_cliente(id: int, datos_nuevos: Cliente):
    for cliente in lista_clientes:
        if cliente.id == id:
            cliente.nombre = datos_nuevos.nombre
            cliente.descripcion = datos_nuevos.descripcion
            return {"mensaje": "Cliente editado correctamente"}
    return {"mensaje": "No se pudo editar porque el cliente no existe"}

@app.delete("/clientes/{id}")
def borrar_cliente(id: int):
    for cliente in lista_clientes:
        if cliente.id == id:
            lista_clientes.remove(cliente)
            return {"mensaje": "Cliente eliminado de la lista"}
    return {"mensaje": "No se encontró el cliente para eliminar"}


# MÓDULO 2: CRUD DE FACTURAS

@app.get("/facturas")
def mostrar_facturas():
    return {"Facturas": lista_facturas}

@app.get("/facturas/{id}")
def buscar_una_factura(id: int):
    for factura in lista_facturas:
        if factura.id == id:
            return {"Factura encontrada": factura}
    return {"mensaje": "No se encontró la factura"}

@app.post("/facturas")
def guardar_factura(datos: Factura):
    lista_facturas.append(datos)
    return {"mensaje": "Factura guardada con éxito"}

@app.put("/facturas/{id}")
def modificar_factura(id: int, datos_nuevos: Factura):
    for factura in lista_facturas:
        if factura.id == id:
            factura.fecha = datos_nuevos.fecha
            factura.valor_total = datos_nuevos.valor_total
            factura.cliente = datos_nuevos.cliente
            return {"mensaje": "Factura editada correctamente"}
    return {"mensaje": "No se pudo editar porque la factura no existe"}

@app.delete("/facturas/{id}")
def borrar_factura(id: int):
    for factura in lista_facturas:
        if factura.id == id:
            lista_facturas.remove(factura)
            return {"mensaje": "Factura eliminada de la lista"}
    return {"mensaje": "No se encontró la factura para eliminar"}


# MÓDULO 3: CRUD DE TRANSACCIONES

@app.get("/transacciones")
def mostrar_transacciones():
    return {"Transacciones": lista_transacciones}

@app.get("/transacciones/{id}")
def buscar_una_transaccion(id: int):
    for transaccion in lista_transacciones:
        if transaccion.id == id:
            return {"Transaccion encontrada": transaccion}
    return {"mensaje": "No se encontró la transaccíon"}

@app.post("/transacciones")
def guardar_transaccion(datos: Transaccion):
    lista_transacciones.append(datos)
    return {"mensaje": "Transación guardada con éxito"}

@app.put("/transacciones/{id}")
def modificar_transaccion(id: int, datos_nuevos: Transaccion):
    for transaccion in lista_transacciones:
        if transaccion.id == id:
            transaccion.vr_unitario = datos_nuevos.vr_unitario
            transaccion.cantidad = datos_nuevos.cantidad
            transaccion.factura_id = datos_nuevos.factura_id
            return {"mensaje": "Transacción editada correctamente"}
    return {"mensaje": "No se pudo editar porque la transacción no existe"}

@app.delete("/transacciones/{id}")
def borrar_transaccion(id: int):
    for transaccion in lista_transacciones:
        if transaccion.id == id:
            lista_transacciones.remove(transaccion)
            return {"mensaje": "Transacción eliminada de la lista"}
    return {"mensaje": "No se encontró la transacción para eliminar"}