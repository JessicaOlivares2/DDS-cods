import csv
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def extract_product_info():
    # Configuración del servicio del driver
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()

    # Inicia el navegador con el servicio y las opciones
    driver = webdriver.Chrome(service=service, options=options)

    # URL del producto en Carrefour
    url = "https://www.carrefour.com.ar/celular-libre-samsung-galaxy-a06-64gb-negro/p"
    driver.get(url)

    # Esperamos a que la página cargue completamente
    wait = WebDriverWait(driver, 20)

    try:
        # Esperar a que el banner de cookies sea clickeable y cerrarlo
        cookie_banner = wait.until(EC.element_to_be_clickable((By.ID, 'onetrust-accept-btn-handler')))
        cookie_banner.click()  # Cierra el banner de cookies

        # Esperar a que el título del producto esté disponible
        product_title = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'span.vtex-breadcrumb-1-x-term')))
        print(f"Título: {product_title.text}")

        # Esperar a que el precio del producto esté disponible
        product_price = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.valtech-carrefourar-product-price-0-x-currencyContainer')))
        print(f"Precio: {product_price.text}")

        # Guardar la información en un archivo CSV
        with open("carrefour_product_info.csv", mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Título", "Precio"])
            writer.writerow([product_title.text, product_price.text])

    except Exception as e:
        print(f"Error inesperado: {e}")
    finally:
        driver.quit()

# Ejecutar la función
extract_product_info()
