from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
from playwright.sync_api import sync_playwright

def extract_product_Dia():
    navegador = webdriver.Firefox()
    navegador.get("https://diaonline.supermercadosdia.com.ar/desayuno/galletitas-y-cereales")
    soup = BeautifulSoup(navegador.page_source, "html.parser")
    products = soup.find_all(
        "section",{ "class":"vtex-product-summary-2-x-container vtex-product-summary-2-x-container--shelf vtex-product-summary-2-x-containerNormal vtex-product-summary-2-x-containerNormal--shelf overflow-hidden br3 h-100 w-100 flex flex-column justify-between center tc"},
        
    )
    productData = []
    for product in products:
        try:
            nombre = product.find("h3").span.text
            precio = product.find("span",{"class":"diaio-store-5-x-sellingPriceValue"}).text
            url_product = product.find("a")["href"]
            productData.append(
                {
                    "Supermercado": "Dia",
                    "Nombre":nombre,
                    "Precio": precio,
                    "Enlace": url_product
                }
            )
        except Exception as e:
            print(f"Error:{e}")
    navegador.close()    
    return productData


def extract_product_Coto():
    with sync_playwright() as p:
        navegador = p.firefox.launch(headless=True) 
        page = navegador.new_page()
        page.goto("https://www.cotodigital.com.ar/sitios/cdigi/categoria/catalogo-limpieza-limpieza-de-cocina-detergentes/_/N-bn6wsg")
        
        
        page_content = page.content()

   # navegador = webdriver.Firefox()
    #navegador.get("https://www.cotodigital.com.ar/sitios/cdigi/categoria/catalogo-limpieza-limpieza-de-cocina-detergentes/_/N-bn6wsg")
        soup = BeautifulSoup(page_content, "html.parser")
        products = soup.find_all("catalogue-product")
        productData = []
    for product in products:
        try:
            nombre = product.find("h3").text
            precio = product.find("h4").text
            url_product = "URL no disponible en este código"
            productData.append(
                {
                    "Supermercado": "Coto",
                    "Nombre":nombre,
                    "Precio": precio,
                    "Enlace": url_product
                }
            )
        except Exception as e:
            print(f"Error:{e}")
    #navegador.close()    
    return productData


def extract_product_Disco():
    navegador = webdriver.Firefox()
    navegador.get("https://www.disco.com.ar/electro/telefonos/celulares")
    soup = BeautifulSoup(navegador.page_source, "html.parser")
    products = soup.find_all(
        "section",{ "class":"vtex-product-summary-2-x-container vtex-product-summary-2-x-containerNormal overflow-hidden br3 h-100 w-100 flex flex-column justify-between center tc"},

    )
    productData = []
    for product in products:
        try:
            nombre = product.find("h2").span.text
            precio = product.find("div",{"class":"discoargentina-store-theme-1dCOMij_MzTzZOCohX1K7w"}).text
            url_product = product.find("a")["href"]
            productData.append(
                {
                    "Supermercado": "Disco",
                    "Nombre":nombre,
                    "Precio": precio,
                    "Enlace": url_product
                }
            )
        except Exception as e:
            print(f"Error:{e}")
    navegador.close()    
    return productData


def main():
    productosDia = extract_product_Dia()
    productosCoto = extract_product_Coto()
    productosDisco = extract_product_Disco()
    df = pd.DataFrame(productosDia + productosCoto + productosDisco)
    df.to_csv("productos_Super.csv", index=False)

main()