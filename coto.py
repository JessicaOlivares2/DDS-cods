import csv
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import traceback
from selenium.common.exceptions import TimeoutException, NoSuchElementException

def extract_product_info():
    # Configuramos el servicio del driver
    service = Service(ChromeDriverManager().install())

    # Configuramos las opciones del navegador
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Ejecutar el navegador en modo headless (sin interfaz gráfica)
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    # Inicia el navegador con el servicio y las opciones
    driver = webdriver.Chrome(service=service, options=options)

    # URL del producto en Coto Digital
    url = "https://www.cotodigital.com.ar/sitios/cdigi/productos/resaltador-filgo-lighter-fine-varios-colores-2-unidades/_/R-00268457-00268457-200"
    driver.get(url)

    try:
        # Esperamos hasta que la información del producto esté disponible
        wait = WebDriverWait(driver, 30)

        # Usamos el XPath correcto para el título del producto
        product_title = wait.until(EC.presence_of_element_located((By.XPATH, "//h2[contains(@class, 'title text-dark')]"))).text
        product_price = driver.find_element(By.XPATH, "//var[contains(@class, 'price h3')]").text
        product_description = driver.find_element(By.XPATH, "//div[contains(@class, 'mb-3')]").text

        # Imprimir la información para verificar
        print(f"Título: {product_title}")
        print(f"Precio: {product_price}")
        print(f"Descripción: {product_description}")

        # Guardar la información en un archivo CSV
        with open("coto_product_info.csv", mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Título", "Precio", "Descripción"])
            writer.writerow([product_title, product_price, product_description])

    except TimeoutException as e:
        print(f"TimeoutException: El elemento no se cargó a tiempo. Error: {e}")
    except NoSuchElementException as e:
        print(f"NoSuchElementException: El elemento no se encontró. Error: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")
        traceback.print_exc()
    finally:
        driver.quit()

# Ejecutar la función
extract_product_info()
