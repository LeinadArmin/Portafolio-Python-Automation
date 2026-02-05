import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

print("--- Iniciando el Espía de Precios ---")

# 1. NAVEGAR AL SITIO WEB
url_objetivo = "http://books.toscrape.com/catalogue/category/books/travel_2/index.html"
print(f"Visitando: {url_objetivo}")

# Hacemos la petición (Python va a la web y se descarga el código HTML)
respuesta = requests.get(url_objetivo)

# Verificamos si la página funcionó (Código 200 = OK)
if respuesta.status_code == 200:
    print("¡Conexión exitosa! Analizando datos...")
    
    # 2. PROCESAR EL HTML (LA "SOPA")
    # Convertimos el texto feo del HTML en un objeto ordenado
    sopa = BeautifulSoup(respuesta.text, 'html.parser')
    
    # Buscamos todos los artículos (libros). 
    # En esta web, cada libro está dentro de una etiqueta <article class="product_pod">
    libros_encontrados = sopa.find_all('article', class_='product_pod')
    
    print(f"Se encontraron {len(libros_encontrados)} libros en esta página.\n")
    
    lista_libros = []
    
    # 3. EXTRAER DATOS UNO POR UNO
    for libro in libros_encontrados:
        # Título: Está dentro de un <h3> y luego un <a>, en el atributo 'title'
        titulo = libro.h3.find('a')['title']
        
        # Precio: Está en un <p class="price_color">
        precio_sucio = libro.find('p', class_='price_color').text
        # Limpiamos el símbolo raro Â£ (libras)
        precio_limpio = precio_sucio.replace('Â£', '')
        
        # Disponibilidad: Buscamos si dice "In stock"
        stock = libro.find('p', class_='instock availability').text.strip()
        
        print(f"Libro detectado: {titulo} | Precio: {precio_limpio}")
        
        # Guardamos en nuestra lista
        lista_libros.append({
            "Título": titulo,
            "Precio (Libras)": precio_limpio,
            "Stock": stock
        })
    
    # 4. EXPORTAR A EXCEL/CSV
    df = pd.DataFrame(lista_libros)
    df.to_csv("Precios_Competencia.csv", index=False, encoding='utf-8-sig') # utf-8-sig es para que Excel lea bien los tildes
    
    print("\n--- ¡Misión Cumplida! ---")
    print("Revisa el archivo 'Precios_Competencia.csv' en tu carpeta.")

else:
    print("Error al conectar con la página. Tal vez cambió la URL.")