import streamlit as st
import pandas as pd
import requests

# Configuración de la página
st.set_page_config(page_title="StockFlow Dashboard", layout="centered")

st.title("📦 Gestión de Bodega - StockFlow")
st.write("Panel de control conectado a tu API FastAPI")

# URL de tu API (el cerebro)
API_URL = "http://127.0.0.1:8000"

# --- SECCIÓN 1: VER INVENTARIO ---
st.header("📋 Inventario en Tiempo Real")

if st.button("🔄 Cargar Productos"):
    try:
        respuesta = requests.get(f"{API_URL}/productos")
        if respuesta.status_code == 200:
            datos = respuesta.json()
            if datos:
                # Convertimos JSON a DataFrame de Pandas (¡Tu especialidad!)
                df = pd.DataFrame(datos)
                
                # Reordenamos columnas para que se vea bonito
                df = df[["id", "nombre", "stock", "precio"]]
                
                # Mostramos la tabla interactiva
                st.dataframe(df, use_container_width=True)
                st.success(f"Se encontraron {len(datos)} productos en bodega.db")
            else:
                st.warning("La bodega está vacía.")
        else:
            st.error("Error: La API respondió, pero hubo un problema.")
    except:
        st.error("❌ Error Crítico: ¿Está encendida la API? (Recuerda ejecutar uvicorn)")

st.divider() # Una línea divisoria visual

# --- SECCIÓN 2: AGREGAR PRODUCTO ---
st.header("➕ Nuevo Ingreso")

col1, col2 = st.columns(2)
with col1:
    nuevo_nombre = st.text_input("Nombre del Producto")
    nuevo_precio = st.number_input("Precio ($)", min_value=0, step=1000)
with col2:
    nuevo_stock = st.number_input("Stock Inicial", min_value=1, step=1)

if st.button("Guardar en Base de Datos"):
    if nuevo_nombre:
        # Preparamos el paquete JSON
        nuevo_producto = {
            "nombre": nuevo_nombre,
            "precio": int(nuevo_precio),
            "stock": int(nuevo_stock)
        }
        
        # Enviamos al Backend (POST)
        res = requests.post(f"{API_URL}/productos", json=nuevo_producto)
        
        if res.status_code == 200:
            st.success(f"¡Éxito! {nuevo_nombre} guardado en bodega.db")
        else:
            st.error("No se pudo guardar.")
    else:
        st.warning("El nombre no puede estar vacío.")