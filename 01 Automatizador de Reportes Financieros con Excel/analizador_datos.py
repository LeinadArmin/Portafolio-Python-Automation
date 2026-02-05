import pandas as pd
import glob  # Librería para buscar archivos (ej: todos los que terminen en .xlsx)

print("--- Iniciando proceso de automatización ---")

# 1. BUSCAR ARCHIVOS
# Buscamos todos los archivos que empiecen con 'ventas_' y terminen en '.xlsx'
archivos_encontrados = glob.glob("ventas_*.xlsx")
print(f"Archivos encontrados: {len(archivos_encontrados)}")

# 2. UNIFICAR DATOS (ETL)
lista_de_tablas = []

for archivo in archivos_encontrados:
    print(f"Leyendo: {archivo}...")
    # Leemos el excel
    df_temporal = pd.read_excel(archivo)
    
    # Truco Pro: Agregamos una columna para saber de qué archivo vino el dato
    # (nos sirve para saber qué sucursal vendió qué)
    nombre_sucursal = archivo.replace("ventas_", "").replace(".xlsx", "")
    df_temporal["Sucursal"] = nombre_sucursal
    
    lista_de_tablas.append(df_temporal)

# 'concat' pega todas las tablas una debajo de la otra
df_total = pd.concat(lista_de_tablas, ignore_index=True)

print(f"Total de ventas unificadas: {len(df_total)} filas.")

# 3. CÁLCULOS Y ANÁLISIS
# Creamos una columna nueva calculada (como en Excel)
df_total["Monto Total"] = df_total["Cantidad"] * df_total["Precio Unitario"]

# Agrupamos por producto para ver cuál vende más (Similar a una Tabla Dinámica)
resumen_productos = df_total.groupby("Producto")[["Cantidad", "Monto Total"]].sum().sort_values("Monto Total", ascending=False)

print("\n--- Resumen Preliminar ---")
print(resumen_productos)

# 4. EXPORTAR REPORTE
nombre_reporte = "Reporte_Consolidado_2026.xlsx"

# Usamos ExcelWriter para guardar dos hojas distintas en el mismo archivo
with pd.ExcelWriter(nombre_reporte, engine='xlsxwriter') as writer:
    # Hoja 1: El detalle completo unificado
    df_total.to_excel(writer, sheet_name="Detalle Completo", index=False)
    
    # Hoja 2: El resumen por producto
    resumen_productos.to_excel(writer, sheet_name="Resumen por Producto")

print(f"\n¡Éxito! Reporte guardado como: {nombre_reporte}")