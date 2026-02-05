from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

print("--- Iniciando Robot con Navegador Real ---")

# 1. CONFIGURAR EL NAVEGADOR
# Esto descarga el driver necesario para tu versión de Chrome automáticamente
options = webdriver.ChromeOptions()
# options.add_argument("--headless") # Si descomentas esto, el navegador no se ve (modo fantasma)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

try:
    # 2. NAVEGAR
    url = "https://listado.mercadolibre.cl/ssd#D[A:ssd]"
    print(f"Abriendo Chrome en: {url}")
    driver.get(url)
    
    # 3. ESPERAR INTELIGENTE
    # Le decimos al robot: "Espera hasta 10 segundos a que aparezca al menos un precio"
    # Esto vence al "loading" infinito
    print("Esperando a que carguen los productos...")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "ui-search-layout__item"))
    )
    
    # Damos un respiro extra para asegurar que todo el texto esté listo
    time.sleep(3)

    # 4. EXTRACCIÓN DE DATOS
    # Buscamos todas las tarjetas de productos (el contenedor li)
    productos = driver.find_elements(By.CLASS_NAME, "ui-search-layout__item")
    print(f"¡Carga completa! Se detectaron {len(productos)} productos.")
    
    lista_datos = []
    
    for prod in productos:
        try:
            # A. TÍTULO
            # Intentamos buscar el título dentro de la tarjeta actual (prod)
            # Usamos una lista de posibles nombres de clase por si acaso
            titulo = "Sin título"
            posibles_clases_titulo = ["poly-component__title", "ui-search-item__title"]
            
            for clase in posibles_clases_titulo:
                elementos = prod.find_elements(By.CLASS_NAME, clase)
                if elementos: # Si encontró algo
                    titulo = elementos[0].text
                    break # Deja de buscar
            
            # B. PRECIO
            # Buscamos el precio actual (contenedor grande)
            precio = "Agotado/No disponible"
            
            # Intentamos encontrar el contenedor del precio
            precios_container = prod.find_elements(By.CLASS_NAME, "poly-price__current")
            if not precios_container:
                 # Intento con diseño antiguo
                 precios_container = prod.find_elements(By.CLASS_NAME, "ui-search-price__part--medium")
            
            if precios_container:
                # Dentro del contenedor, buscamos el número exacto
                montos = precios_container[0].find_elements(By.CLASS_NAME, "andes-money-amount__fraction")
                if montos:
                    precio = montos[0].text
            
            print(f"Detectado: {titulo[:30]}... | {precio}")
            
            lista_datos.append({
                "Producto": titulo,
                "Precio": precio
            })
            
        except Exception as e:
            print(f"Error en un producto: {e}")
            continue

    # 5. GUARDAR
    if lista_datos:
        df = pd.DataFrame(lista_datos)
        df.to_csv("Precios_SSD_Selenium.csv", index=False, encoding='utf-8-sig', sep=';')
        print(f"\n✅ ÉXITO: Archivo 'Precios_SSD_Selenium.csv' guardado.")
    else:
        print("⚠️ No se pudieron extraer datos.")

except Exception as e:
    print(f"❌ Error crítico: {e}")

finally:
    # Cerramos el navegador al terminar
    print("Cerrando navegador...")
    driver.quit()