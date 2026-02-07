from fastapi import FastAPI, HTTPException
from sqlmodel import SQLModel, Field, Session, select, create_engine
from typing import Optional, List

# 1. CONFIGURACIÓN DE LA BASE DE DATOS
# Esto creará un archivo real llamado 'bodega.db' en tu carpeta
nombre_archivo = "bodega.db"
url_base_datos = f"sqlite:///{nombre_archivo}"

# El "motor" que conecta Python con el archivo
engine = create_engine(url_base_datos)

# 2. MODELO DE DATOS (LA TABLA)
# table=True le dice a SQLModel que esto es una tabla real en la base de datos
class Producto(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True) # Llave primaria (ID único)
    nombre: str
    stock: int
    precio: int

# 3. INICIALIZAR LA APP
app = FastAPI()

# Esto se ejecuta una sola vez al prender el servidor:
# Crea la tabla si no existe
@app.on_event("startup")
def crear_tablas():
    SQLModel.metadata.create_all(engine)

# --- RUTAS (ENDPOINTS) ---

@app.get("/")
def home():
    return {"mensaje": "API de Bodega con Base de Datos SQL v2.0"}

# A. CREAR PRODUCTO (POST) -> Ahora guarda en el archivo .db
@app.post("/productos", response_model=Producto)
def crear_producto(producto: Producto):
    with Session(engine) as sesion:
        sesion.add(producto)    # Preparamos el producto
        sesion.commit()         # Guardamos los cambios (Botón "Guardar")
        sesion.refresh(producto) # Recargamos para obtener el ID generado automáticament
        return producto

# B. LEER TODOS (GET) -> Lee desde el archivo
@app.get("/productos", response_model=List[Producto])
def obtener_productos():
    with Session(engine) as sesion:
        # Traduce: "SELECT * FROM producto"
        consulta = select(Producto)
        resultados = sesion.exec(consulta).all()
        return resultados

# C. BUSCAR POR ID (GET)
@app.get("/productos/{producto_id}", response_model=Producto)
def obtener_producto(producto_id: int):
    with Session(engine) as sesion:
        producto = sesion.get(Producto, producto_id)
        if not producto:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        return producto

# D. BORRAR PRODUCTO (DELETE) - ¡Nuevo!
@app.delete("/productos/{producto_id}")
def borrar_producto(producto_id: int):
    with Session(engine) as sesion:
        producto = sesion.get(Producto, producto_id)
        if not producto:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        
        sesion.delete(producto) # Borramos
        sesion.commit()         # Confirmamos
        return {"mensaje": "Producto eliminado correctamente"}