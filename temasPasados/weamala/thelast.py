import csv
import pandas as pd
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import traceback
from selenium.common.exceptions import TimeoutException

CSV_FILENAME = "productos.csv"
data_list = [] 

def setup_driver():
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Sin interfaz gráfica
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    return webdriver.Chrome(service=service, options=options)

def save_to_dataframe(data):
    data_list.append(data)

def save_to_csv():
    df = pd.DataFrame(data_list, columns=["Supermercado", "Producto", "Precio", "Descripción", "URL"])
    
    df.to_csv(CSV_FILENAME, index=False, encoding="utf-8")
    print(f"Datos guardados en {CSV_FILENAME}")

def extract_product_info_coto():
    driver = setup_driver()
    url = "https://www.cotodigital.com.ar/sitios/cdigi/productos/resaltador-filgo-lighter-fine-varios-colores-2-unidades/_/R-00268457-00268457-200"
    driver.get(url)

    try:
        wait = WebDriverWait(driver, 60)

        product_title = wait.until(EC.presence_of_element_located((By.XPATH, "//h2[contains(@class, 'title text-dark')]"))).text
        product_price = driver.find_element(By.XPATH, "//var[contains(@class, 'price h3')]").text
        product_description = driver.find_element(By.XPATH, "//div[contains(@class, 'mb-3')]").text

        print(f"[COTO] {product_title} - {product_price}")

        save_to_dataframe(["Coto", product_title, product_price, product_description, url])

    except Exception as e:
        print(f"Error en Coto: {e}")
        traceback.print_exc()
    finally:
        driver.quit()

def extract_product_info_dia():
    driver = setup_driver()
    url = "https://diaonline.supermercadosdia.com.ar/galletitas-pepitos-con-chips-de-chocolate-357g-pack-x-3-ud-de-119-gr-271632/p"
    driver.get(url)

    try:
        wait = WebDriverWait(driver, 60)

        product_title = wait.until(EC.presence_of_element_located((By.XPATH, "//span[contains(@class, 'vtex-store-components-3-x-productBrand')]"))).text
        product_price = driver.find_element(By.XPATH, "//span[contains(@class, 'diaio-store-5-x-sellingPrice')]").text

        print(f"[DÍA] {product_title} - {product_price}")

        save_to_dataframe(["Día", product_title, product_price, "N/A", url])

    except Exception as e:
        print(f"Error en Día: {e}")
        traceback.print_exc()
    finally:
        driver.quit()

def extract_product_info_carrefour():
    driver = setup_driver()
    url = "https://www.carrefour.com.ar/celular-libre-samsung-galaxy-a06-64gb-negro/p"
    driver.get(url)

    try:
        wait = WebDriverWait(driver, 60)

        # Cierra el banner de cookies si aparece
        try:
            cookie_banner = wait.until(EC.element_to_be_clickable((By.ID, 'onetrust-accept-btn-handler')))
            cookie_banner.click()
        except TimeoutException:
            print("No se encontró banner de cookies en Carrefour, continuando...")

        product_title = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'span.vtex-breadcrumb-1-x-term'))).text
        product_price = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.valtech-carrefourar-product-price-0-x-currencyContainer'))).text

        print(f"[CARREFOUR] {product_title} - {product_price}")

        save_to_dataframe(["Carrefour", product_title, product_price, "N/A", url])

    except Exception as e:
        print(f"Error en Carrefour: {e}")
        traceback.print_exc()
    finally:
        driver.quit()

def main():
    print("Iniciando extracción de datos...")
    extract_product_info_coto()
    extract_product_info_dia()
    extract_product_info_carrefour()
    save_to_csv()  
    print("Extracción completada. Datos guardados en productos.csv.")

if __name__ == "__main__":
    main()
