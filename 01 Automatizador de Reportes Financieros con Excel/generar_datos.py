import pandas as pd
import random
from datetime import datetime, timedelta

# Configuración básica
sucursales = ['Norte', 'Centro', 'Sur']
productos = ['Teclado Mecánico', 'Mouse Gamer', 'Monitor 24"', 'Laptop', 'Headset']

def crear_datos_falsos(nombre_sucursal):
    datos = []
    # Generar 50 ventas falsas para cada sucursal
    for _ in range(50):
        fecha = datetime(2024, 1, 1) + timedelta(days=random.randint(0, 30))
        producto = random.choice(productos)
        cantidad = random.randint(1, 5)
        precio_unitario = random.randint(20000, 150000)
        
        datos.append({
            "Fecha": fecha.strftime("%Y-%m-%d"),
            "Producto": producto,
            "Cantidad": cantidad,
            "Precio Unitario": precio_unitario,
            "Vendedor": f"Vendedor_{random.randint(1, 5)}"
        })
    
    df = pd.DataFrame(datos)
    # Guardamos el excel: "ventas_Norte.xlsx", etc.
    nombre_archivo = f"ventas_{nombre_sucursal}.xlsx"
    df.to_excel(nombre_archivo, index=False)
    print(f"Archivo generado: {nombre_archivo}")

# Crear los 3 archivos
for sucursal in sucursales:
    crear_datos_falsos(sucursal)

print("¡Archivos de prueba listos!")