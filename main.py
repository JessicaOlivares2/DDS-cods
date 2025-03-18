import csv
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import traceback
from selenium.common.exceptions import TimeoutException, NoSuchElementException

def extract_product_info_dia():
    # Configuración del servicio del driver
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Ejecutar el navegador en modo headless (sin interfaz gráfica)
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    # Inicia el navegador con el servicio y las opciones
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # URL del producto en Día
        url = "https://diaonline.supermercadosdia.com.ar/galletitas-pepitos-con-chips-de-chocolate-357g-pack-x-3-ud-de-119-gr-271632/p"
        driver.get(url)
        
        wait = WebDriverWait(driver, 60)
        
        # Extraemos el nombre del producto, el precio y la URL
        product_title = wait.until(EC.presence_of_element_located((By.XPATH, "//span[contains(@class, 'vtex-store-components-3-x-productBrand vtex-store-components-3-x-productBrand--productNamePdp ')]"))).text
        product_price = driver.find_element(By.XPATH, "//span[contains(@class, 'diaio-store-5-x-sellingPrice')]").text
        product_url = driver.current_url

        # Guardamos la información en el CSV
        with open('productos.csv', mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Supermercado", "Producto", "Precio", "URL"])  # Encabezado del CSV
            writer.writerow(["DIA", product_title, product_price, product_url])
    
    except Exception as e:
        print(f"Error al extraer la información de DIA: {e}")
        traceback.print_exc()
    
    finally:
        driver.quit()

def extract_product_info_coto():
    # Configuración del servicio del driver
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Ejecutar el navegador en modo headless (sin interfaz gráfica)

    # Inicia el navegador con el servicio y las opciones
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # URL del producto en Coto
        url = "https://www.cotodigital.com.ar/sitios/cdigi/productos/resaltador-filgo-lighter-fine-varios-colores-2-unidades/_/R-00268457-00268457-200"
        driver.get(url)
        
        wait = WebDriverWait(driver, 30)
        
        # Extraemos el nombre del producto, el precio y la URL
        product_title = wait.until(EC.presence_of_element_located((By.XPATH, "//h2[contains(@class, 'title text-dark')]"))).text
        product_price = driver.find_element(By.XPATH, "//var[contains(@class, 'price h3')]").text
        product_url = driver.current_url
        
        # Guardamos la información en el CSV
        with open('productos.csv', mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Supermercado", "Producto", "Precio", "URL"])  # Encabezado del CSV
            writer.writerow(["COTO", product_title, product_price, product_url])

    except Exception as e:
        print(f"Error al extraer la información de Coto: {e}")
        traceback.print_exc()

    finally:
        driver.quit()

def extract_product_info_carrefour():
    # Configuración del servicio del driver
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()

    # Inicia el navegador con el servicio y las opciones
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # URL del producto en Carrefour
        url = "https://www.carrefour.com.ar/celular-libre-samsung-galaxy-a06-64gb-negro/p"
        driver.get(url)
        
        wait = WebDriverWait(driver, 20)

        # Esperar a que el banner de cookies sea clickeable y cerrarlo
        cookie_banner = wait.until(EC.element_to_be_clickable((By.ID, 'onetrust-accept-btn-handler')))
        cookie_banner.click()  # Cierra el banner de cookies

        # Extraemos el nombre del producto, el precio y la URL
        product_title = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'span.vtex-breadcrumb-1-x-term'))).text
        product_price = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.valtech-carrefourar-product-price-0-x-currencyContainer'))).text
        product_url = driver.current_url

        # Guardamos la información en el CSV
        with open('productos.csv', mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Supermercado", "Producto", "Precio", "URL"])  # Encabezado del CSV
            writer.writerow(["Carrefour", product_title, product_price, product_url])

    except Exception as e:
        print(f"Error al extraer la información de Carrefour: {e}")
        traceback.print_exc()

    finally:
        driver.quit()

def main():
    # Crear archivo CSV vacío con encabezado si no existe
    with open('productos.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Supermercado", "Producto", "Precio", "URL"])  # Encabezado del CSV

    # Extraer la información de los tres supermercados
    extract_product_info_dia()
    extract_product_info_coto()
    extract_product_info_carrefour()

if __name__ == "__main__":
    main()
