📚 README.md - Sistema de Facturación FastAPI
# 🚀 SISTEMA DE FACTURACIÓN - FASTAPI

## 📌 Descripción
API RESTful para la gestión de clientes, facturas y transacciones, desarrollada con FastAPI y Pydantic. El sistema permite realizar operaciones CRUD completas con validaciones de integridad referencial.

## 🛠️ Tecnologías Utilizadas
- **FastAPI** - Framework web moderno
- **Pydantic** - Validación de datos
- **Uvicorn** - Servidor ASGI
- **Python 3.9+**

---

## 📋 ÍNDICE DE DOCUMENTACIÓN

1. [Estructura del Proyecto](#1-estructura-del-proyecto)
2. [Instalación y Configuración](#2-instalación-y-configuración)
3. [Modelos de Datos](#3-modelos-de-datos)
4. [Endpoints de Clientes](#4-endpoints-de-clientes)
5. [Endpoints de Facturas](#5-endpoints-de-facturas)
6. [Endpoints de Transacciones](#6-endpoints-de-transacciones)
7. [Ejemplos de Uso](#7-ejemplos-de-uso)


---

## 1️⃣ ESTRUCTURA DEL PROYECTO
FASTAPI/
├── app/ # Carpeta principal de la aplicación
│ ├── init.py # Convierte app en paquete Python
│ ├── main.py # Configuración principal de FastAPI
│ ├── database.py # Base de datos en memoria (listas)
│ ├── models/ # Modelos Pydantic
│ │ ├── init.py
│ │ ├── cliente.py # Modelo Cliente
│ │ ├── factura.py # Modelo Factura
│ │ └── transaccion.py # Modelo Transacción
│ └── routers/ # Endpoints y rutas
│ ├── init.py
│ ├── clientes.py # CRUD Clientes
│ ├── facturas.py # CRUD Facturas
│ └── transacciones.py # CRUD Transacciones
├── mi_env/ # Entorno virtual
├── .gitignore # Archivos ignorados por Git
├── requirements.txt # Dependencias del proyecto
├── README.md # Documentación
└── app.py # Versión inicial (sin estructura)


---

## 2️⃣ INSTALACIÓN Y CONFIGURACIÓN

### Paso 1: Clonar el repositorio
```bash
git clone [URL_DEL_REPOSITORIO]
cd FASTAPI

# Crear entorno virtual
python -m venv mi_env

# Activar entorno virtual (Windows)
mi_env\Scripts\activate

# Activar entorno virtual (Mac/Linux)
source mi_env/bin/activate

# Instalar FastAPI y servidor
pip install fastapi uvicorn

# Generar requirements.txt
pip freeze > requirements.txt

# Desde la raíz del proyecto
uvicorn app.main:app --reload

# El servidor estará disponible en:
# http://localhost:8000

3️⃣ MODELOS DE DATOS
📌 Cliente

class Cliente(BaseModel):
    id: int                      # Identificador único
    nombre: str                  # Nombre del cliente
    descripcion: str | None = None  # Descripción opcional

📌 Factura

class Factura(BaseModel):
    id: int                      # Identificador único
    fecha: str                   # Fecha de la factura
    valor_total: float           # Monto total
    cliente: str                 # Nombre del cliente (relación)

📌 Transacción

class Transaccion(BaseModel):
    id: int                      # Identificador único
    vr_unitario: float           # Precio unitario
    cantidad: int                # Cantidad de productos
    factura_id: int              # ID de la factura (relación)

4️⃣ ENDPOINTS DE CLIENTES


Método	Endpoint	Descripción	Estado
GET	/clientes	Listar todos los clientes	200 OK
GET	/clientes/{id}	Obtener cliente por ID	200 OK
POST	/clientes	Crear nuevo cliente	201 Created
PUT	/clientes/{id}	Actualizar cliente	200 OK
DELETE	/clientes/{id}	Eliminar cliente	200 OK
🔍 Validaciones
ID único: No se permite duplicar IDs

📝 Ejemplos
// POST /clientes
{
  "id": 1,
  "nombre": "Juan Perez",
  "descripcion": "Cliente VIP"
}

// GET /clientes/1
{
  "id": 1,
  "nombre": "Juan Perez",
  "descripcion": "Cliente VIP"
}

5️⃣ ENDPOINTS DE FACTURAS
Método	Endpoint	Descripción	Estado
GET	/facturas	Listar todas las facturas	200 OK
GET	/facturas/{id}	Obtener factura por ID	200 OK
POST	/facturas	Crear nueva factura	201 Created
PUT	/facturas/{id}	Actualizar factura	200 OK
DELETE	/facturas/{id}	Eliminar factura	200 OK
🔍 Validaciones
ID único: No se permite duplicar IDs

Cliente existente: El cliente debe estar registrado en lista_clientes

📝 Ejemplos
// POST /facturas
{
  "id": 1,
  "fecha": "2026-07-03",
  "valor_total": 150.50,
  "cliente": "Juan Perez"
}

// ❌ Error si cliente no existe
{
  "detail": "No se puede crear la factura. El cliente 'xxx' no existe."
}
6️⃣ ENDPOINTS DE TRANSACCIONES
Método	Endpoint	Descripción	Estado
GET	/transacciones	Listar todas las transacciones	200 OK
GET	/transacciones/{id}	Obtener transacción por ID	200 OK
POST	/transacciones	Crear nueva transacción	201 Created
PUT	/transacciones/{id}	Actualizar transacción	200 OK
DELETE	/transacciones/{id}	Eliminar transacción	200 OK
🔍 Validaciones
ID único: No se permite duplicar IDs

Factura existente: La factura debe estar registrada en lista_facturas

📝 Ejemplos

// POST /transacciones
{
  "id": 1,
  "vr_unitario": 50.00,
  "cantidad": 3,
  "factura_id": 1
}

// ❌ Error si factura no existe
{
  "detail": "No se puede registrar la transacción. La factura con ID 1 no existe."
}

7️⃣ EJEMPLOS DE USO
🔄 Flujo Completo de una Venta

# 1. Registrar cliente
curl -X POST "http://localhost:8000/clientes" \
  -H "Content-Type: application/json" \
  -d '{"id": 1, "nombre": "María Gómez", "descripcion": "Cliente frecuente"}'

# 2. Crear factura
curl -X POST "http://localhost:8000/facturas" \
  -H "Content-Type: application/json" \
  -d '{"id": 1, "fecha": "2026-07-03", "valor_total": 0, "cliente": "María Gómez"}'

# 3. Agregar productos (transacciones)
curl -X POST "http://localhost:8000/transacciones" \
  -H "Content-Type: application/json" \
  -d '{"id": 1, "vr_unitario": 100.00, "cantidad": 2, "factura_id": 1}'

curl -X POST "http://localhost:8000/transacciones" \
  -H "Content-Type: application/json" \
  -d '{"id": 2, "vr_unitario": 50.00, "cantidad": 1, "factura_id": 1}'

# 4. Consultar información
curl "http://localhost:8000/clientes"          # Ver clientes
curl "http://localhost:8000/facturas"          # Ver facturas
curl "http://localhost:8000/transacciones"     # Ver transacciones

✅ Pruebas de Validaciones

# ❌ Crear factura con cliente inexistente (Error 400)
curl -X POST "http://localhost:8000/facturas" \
  -H "Content-Type: application/json" \
  -d '{"id": 99, "fecha": "2026-07-03", "valor_total": 100, "cliente": "Inexistente"}'

# ❌ Crear transacción con factura inexistente (Error 400)
curl -X POST "http://localhost:8000/transacciones" \
  -H "Content-Type: application/json" \
  -d '{"id": 99, "vr_unitario": 50, "cantidad": 2, "factura_id": 999}'