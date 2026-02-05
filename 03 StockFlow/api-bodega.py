from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional

# Iniciamos la aplicación (nuestra máquina expendedora)
app = FastAPI()

# --- MODELOS DE DATOS ---
# Definimos las reglas: Un producto DEBE tener nombre (texto) y precio (número)
class Producto(BaseModel):
    id: Optional[int] = None
    nombre: str
    stock: int
    precio: int

# --- BASE DE DATOS SIMULADA ---
# Por ahora usaremos una lista simple en memoria
inventario = [
    {"id": 1, "nombre": "Laptop Gamer", "stock": 5, "precio": 1500000},
    {"id": 2, "nombre": "Mouse Inalámbrico", "stock": 20, "precio": 15000}
]

# --- RUTAS (Lo que la máquina sabe hacer) ---

# 1. Saludo básico (Para ver si funciona)
@app.get("/")
def home():
    return {"mensaje": "Bienvenido al Sistema Bode-Py v1.0"}

# 2. Ver todos los productos
@app.get("/productos")
def obtener_productos():
    return inventario

# 3. Buscar un producto específico por ID
@app.get("/productos/{producto_id}")
def obtener_producto_por_id(producto_id: int):
    # Buscamos en la lista uno por uno
    for producto in inventario:
        if producto["id"] == producto_id:
            return producto
    return {"error": "Producto no encontrado"}

# 4. Agregar producto nuevo (El más interesante)
@app.post("/productos")
def crear_producto(nuevo_producto: Producto):
    # Calculamos el ID nuevo (el último + 1)
    nuevo_id = len(inventario) + 1
    
    # Convertimos los datos recibidos a diccionario
    producto_dict = nuevo_producto.dict()
    producto_dict["id"] = nuevo_id
    
    # Guardamos
    inventario.append(producto_dict)
    return {"mensaje": "Producto registrado", "producto": producto_dict}