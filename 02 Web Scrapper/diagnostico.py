import requests
from bs4 import BeautifulSoup

url = "https://listado.mercadolibre.cl/ssd" # Usaremos la URL limpia sin el #D[A:ssd] para evitar problemas

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'es-ES,es;q=0.9',
    'Referer': 'https://www.google.com/'
}

print(f"--- DIAGNÓSTICO DE CONEXIÓN ---")
print(f"Visitando: {url}")

try:
    response = requests.get(url, headers=headers)
    print(f"Estado de respuesta: {response.status_code}") # Esperamos un 200

    if response.status_code == 200:
        # Guardamos lo que ve el robot en un archivo HTML
        with open("lo_que_ve_el_robot.html", "w", encoding="utf-8") as f:
            f.write(response.text)
        print("✅ Se guardó el archivo 'lo_que_ve_el_robot.html'.")
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # PRUEBAS DE SELECTORES
        # 1. Buscamos contenedores antiguos
        items_old = soup.find_all('li', class_='ui-search-layout__item')
        print(f"Prueba 1 (Diseño Clásico): Encontrados {len(items_old)} elementos.")
        
        # 2. Buscamos contenedores nuevos (Poly)
        items_poly = soup.find_all('div', class_='poly-card')
        print(f"Prueba 2 (Diseño Poly): Encontrados {len(items_poly)} elementos.")
        
        # 3. Buscamos títulos directamente (a lo bruto)
        titulos = soup.find_all('h2', class_='poly-component__title')
        if len(titulos) == 0:
             titulos = soup.find_all('h2', class_='ui-search-item__title')
        print(f"Prueba 3 (Solo Títulos): Encontrados {len(titulos)} elementos.")

    else:
        print("❌ Mercado Libre rechazó la conexión.")

except Exception as e:
    print(f"❌ Error crítico: {e}")