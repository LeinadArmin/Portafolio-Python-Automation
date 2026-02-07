from fastapi import FastAPI, HTTPException, Depends, status # <--- Agregamos Depends y status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm # <--- Para el candado en la documentación
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

# 🔐 CONFIGURACIÓN DE SEGURIDAD
# Esta es tu llave maestra. En la vida real, esto se guarda en variables de entorno (.env)
MI_TOKEN_SECRETO = "supersecreto123"

# Esto hace que aparezca el candadito en la documentación automática
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verificar_token(token: str = Depends(oauth2_scheme)):
    if token != MI_TOKEN_SECRETO:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido. Acceso denegado.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token





# Esto se ejecuta una sola vez al prender el servidor:
# Crea la tabla si no existe
@app.on_event("startup")
def crear_tablas():
    SQLModel.metadata.create_all(engine)

# --- RUTA DE LOGIN (SIMULADA) ---
# Esta es la ventanilla que Swagger necesita para el botón "Authorize"
@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # En un sistema real, aquí verificaríamos usuario y contraseña en la BD.
    # Por ahora, simplemente devolvemos la llave maestra a quien la pida.
    return {"access_token": MI_TOKEN_SECRETO, "token_type": "bearer"}

# --- RUTAS (ENDPOINTS) ---

@app.get("/")
def home():
    return {"mensaje": "API de Bodega con Base de Datos SQL v2.0"}

@app.get("/productos", response_model=List[Producto])
def obtener_productos():
    with Session(engine) as sesion:
        # Traduce: "SELECT * FROM producto"
        consulta = select(Producto)
        resultados = sesion.exec(consulta).all()
        return resultados

@app.get("/productos/{producto_id}", response_model=Producto)
def obtener_producto(producto_id: int):
    with Session(engine) as sesion:
        producto = sesion.get(Producto, producto_id)
        if not producto:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        return producto

@app.post("/productos", response_model=Producto, dependencies=[Depends(verificar_token)]) 
def crear_producto(producto: Producto):
    with Session(engine) as sesion:
        sesion.add(producto)
        sesion.commit()
        sesion.refresh(producto)
        return producto

@app.delete("/productos/{producto_id}", dependencies=[Depends(verificar_token)])
def borrar_producto(producto_id: int):
    with Session(engine) as sesion:
        producto = sesion.get(Producto, producto_id)
        if not producto:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        sesion.delete(producto)
        sesion.commit()
        return {"mensaje": "Producto eliminado"}