import requests
from bs4 import BeautifulSoup
import pandas as pd

print("--- Iniciando Espía de SSDs en Mercado Libre ---")

# 1. URL ESPECÍFICA (La que me pasaste)
url_objetivo = "https://listado.mercadolibre.cl/ssd#D[A:ssd]"

# HEADERS: Indispensable para que no nos bloqueen
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

print(f"Visitando: {url_objetivo}")
respuesta = requests.get(url_objetivo, headers=headers)

if respuesta.status_code == 200:
    sopa = BeautifulSoup(respuesta.text, 'html.parser')
    
    # 2. BUSCAR LAS TARJETAS DE PRODUCTO
    # En tu captura se ve el diseño nuevo "Poly".
    # Usualmente las tarjetas siguen siendo elementos de lista (li)
    productos = sopa.find_all('li', class_='ui-search-layout__item')
    
    # Si no encuentra nada con 'li', intentamos con 'div' (plan de respaldo)
    if len(productos) == 0:
        productos = sopa.find_all('div', class_='ui-search-result__wrapper')

    print(f"Se encontraron {len(productos)} productos.\n")
    
    lista_datos = []
    
    for producto in productos:
        try:
            # A. TÍTULO
            # En el diseño de tu foto, el título suele ser 'poly-component__title'
            titulo_elem = producto.find('h2', class_='poly-component__title')
            # Respaldo por si acaso es un enlace (a) en vez de h2
            if not titulo_elem:
                titulo_elem = producto.find('a', class_='poly-component__title')
            
            # Si aún no lo encuentra, probamos la clase antigua
            if not titulo_elem:
                titulo_elem = producto.find('h2', class_='ui-search-item__title')
                
            titulo = titulo_elem.text.strip() if titulo_elem else "Título no detectado"
            
            # B. PRECIO (Basado en tu inspección de imagen 3)
            # Buscamos el contenedor del precio actual
            precio_container = producto.find('div', class_='poly-price__current')
            
            if precio_container:
                # Buscamos la fracción del precio (el número 24.990)
                monto = precio_container.find('span', class_='andes-money-amount__fraction')
                precio = monto.text.strip() if monto else "Precio no legible"
            else:
                precio = "Agotado"

            # C. LINK
            link_elem = producto.find('a')
            link = link_elem['href'] if link_elem else "Sin link"

            print(f"Detectado: {titulo[:40]}... | Precio: {precio}")
            
            lista_datos.append({
                "Producto": titulo,
                "Precio": precio,
                "Link": link
            })
            
        except Exception as e:
            continue

    # GUARDAR
    if len(lista_datos) > 0:
        df = pd.DataFrame(lista_datos)
        df.to_csv("Precios_SSD.csv", index=False, encoding='utf-8-sig')
        print(f"\n¡Éxito! Se guardaron {len(lista_datos)} productos en 'Precios_SSD.csv'")
    else:
        print("\nNo se pudieron extraer datos. Mercado Libre pudo haber cambiado el código HTML.")

else:
    print(f"Error de conexión: {respuesta.status_code}")