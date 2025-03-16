from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

# Configurar Selenium
options = webdriver.ChromeOptions()
options.add_argument("--headless")  
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# URLs de supermercados
supermercados_Url = {
    "DIA": "https://www.supermercadosdia.com.ar/",
    "COTO": "https://www.cotodigital3.com.ar/",
    "Carrefour": "https://www.carrefour.com.ar/"
}

productos_lista = []

# Iniciar el navegador
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

for nombre_supermercado, url in supermercados_Url.items():
    print(f"Extrayendo datos de {nombre_supermercado}...")

    driver.get(url)

    try:
        # Esperar que los productos carguen (AJUSTA LA CLASE SEGÚN EL HTML)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "vtex-flex-layout-0-x-flexColChild pb0"))  # CAMBIA ESTO CON LA CLASE CORRECTA
        )

        productos = driver.find_elements(By.CLASS_NAME, "vtex-flex-layout-0-x-flexCol  ml0 mr0 pl0 pr0      flex flex-column h-100 w-100")  # CAMBIA ESTO CON LA CLASE CORRECTA
        
        for producto in productos:
            try:
                nombre = producto.find_element(By.CLASS_NAME, "vtex-product-summary-2-x-nameContainer flex items-start justify-center pv6").text.strip()  # CAMBIA ESTO
                precio = producto.find_element(By.CLASS_NAME, "product-price").text.strip()  # CAMBIA ESTO
                enlace = producto.find_element(By.CLASS_NAME, "product-link").get_attribute("href")  # CAMBIA ESTO

                productos_lista.append([nombre_supermercado, nombre, precio, enlace])
            except Exception as e:
                print(f"Error extrayendo producto: {e}")
                continue
    except Exception as e:
        print(f"No se encontraron productos en {nombre_supermercado}: {e}")

driver.quit()

# Guardar datos en CSV
df = pd.DataFrame(productos_lista, columns=["Supermercado", "Producto", "Precio", "URL"])
df.to_csv("productos_supermercados.csv", index=False, encoding="utf-8")

print("Datos guardados en 'productos_supermercados.csv'")
