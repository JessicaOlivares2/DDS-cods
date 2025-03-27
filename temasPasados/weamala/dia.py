import csv
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import traceback

def extract_product_info():
    # Configuramos el servicio del driver
    service = Service(ChromeDriverManager().install())

    # Configuramos las opciones del navegador
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Ejecutar el navegador en modo headless (sin interfaz gráfica)
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    # Inicia el navegador con el servicio y las opciones
    driver = webdriver.Chrome(service=service, options=options)

    # Establece un tiempo de espera explícito
    driver.set_page_load_timeout(120)  # Aumentamos el tiempo de espera

    try:
        # Abrimos la página del producto específico
        driver.get("https://diaonline.supermercadosdia.com.ar/galletitas-pepitos-con-chips-de-chocolate-357g-pack-x-3-ud-de-119-gr-271632/p")

        # Esperamos hasta que la información del producto esté disponible
        wait = WebDriverWait(driver, 60)  # Aumenta el tiempo de espera
        product_title = wait.until(EC.presence_of_element_located((By.XPATH, "//span[contains(@class, 'vtex-store-components-3-x-productBrand vtex-store-components-3-x-productBrand--productNamePdp ')]"))).text
        product_price = driver.find_element(By.XPATH, "//span[contains(@class, 'diaio-store-5-x-sellingPrice')]").text
        product_description = driver.find_element(By.XPATH, "//div[contains(@class, 'vtex-store-components-3-x-content h-auto')]").text

        # Imprimimos la información extraída (para comprobar que todo esté correcto)
        print(f"Producto: {product_title}")
        print(f"Precio: {product_price}")
        print(f"Descripción: {product_description}")

        # Guardamos la información extraída en un archivo CSV
        with open('productos_dia.csv', mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            # Escribe los encabezados solo si el archivo está vacío (esto evita duplicar encabezados)
            if file.tell() == 0:
                writer.writerow(["Nombre", "Precio", "Descripción"])  # Encabezado del CSV
            # Escribe los datos del producto
            writer.writerow([product_title, product_price, product_description])

    except Exception as e:
        print(f"Error al extraer la información del producto: {e}")
        traceback.print_exc()  # Imprime el seguimiento completo del error

    finally:
        try:
            # Cerramos el driver de Selenium después de usarlo
            driver.quit()
        except Exception as quit_error:
            print(f"Error al cerrar el navegador: {quit_error}")

def main():
    extract_product_info()

if __name__ == "__main__":
    main()
