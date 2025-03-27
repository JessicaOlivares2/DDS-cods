import csv
import pandas as pd  # Agregamos pandas para manejar los datos
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import traceback
from selenium.common.exceptions import TimeoutException, NoSuchElementException

CSV_FILENAME = "productos.csv"

def setup_driver():
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Sin interfaz gráfica
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    return webdriver.Chrome(service=service, options=options)

def extract_products_coto():
    driver = setup_driver()
    url = "https://www.cotodigital.com.ar/sitios/cdigi/browse"  # Página de listado de productos
    driver.get(url)
    data = []
    
    try:
        wait = WebDriverWait(driver, 30)
        products = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'product')]")))
        
        for product in products:
            try:
                title = product.find_element(By.XPATH, ".//h2").text
                price = product.find_element(By.XPATH, ".//var").text
                url = product.find_element(By.XPATH, ".//a").get_attribute("href")
                data.append(["Coto", title, price, url])
            except NoSuchElementException:
                continue
        
    except Exception as e:
        print(f"Error en Coto: {e}")
        traceback.print_exc()
    finally:
        driver.quit()
    
    return data

def extract_products_dia():
    driver = setup_driver()
    url = "https://diaonline.supermercadosdia.com.ar/"  # Página de listado de productos
    driver.get(url)
    data = []
    
    try:
        wait = WebDriverWait(driver, 30)
        products = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'product')]")))
        
        for product in products:
            try:
                title = product.find_element(By.XPATH, ".//span[contains(@class, 'product-title')]").text
                price = product.find_element(By.XPATH, ".//span[contains(@class, 'product-price')]").text
                url = product.find_element(By.XPATH, ".//a").get_attribute("href")
                data.append(["Día", title, price, url])
            except NoSuchElementException:
                continue
        
    except Exception as e:
        print(f"Error en Día: {e}")
        traceback.print_exc()
    finally:
        driver.quit()
    
    return data

def extract_products_carrefour():
    driver = setup_driver()
    url = "https://www.carrefour.com.ar/"  # Página de listado de productos
    driver.get(url)
    data = []
    
    try:
        wait = WebDriverWait(driver, 30)
        products = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'product')]")))
        
        for product in products:
            try:
                title = product.find_element(By.XPATH, ".//span[contains(@class, 'product-title')]").text
                price = product.find_element(By.XPATH, ".//span[contains(@class, 'product-price')]").text
                url = product.find_element(By.XPATH, ".//a").get_attribute("href")
                data.append(["Carrefour", title, price, url])
            except NoSuchElementException:
                continue
        
    except Exception as e:
        print(f"Error en Carrefour: {e}")
        traceback.print_exc()
    finally:
        driver.quit()
    
    return data

def save_to_csv(data):
    df = pd.DataFrame(data, columns=["Supermercado", "Producto", "Precio", "URL"])
    df.to_csv(CSV_FILENAME, index=False, encoding="utf-8")

def main():
    print("Iniciando extracción de datos...")
    data = []
    data.extend(extract_products_coto())
    data.extend(extract_products_dia())
    data.extend(extract_products_carrefour())
    save_to_csv(data)
    print("Extracción completada. Datos guardados en productos.csv.")

if __name__ == "__main__":
    main()
