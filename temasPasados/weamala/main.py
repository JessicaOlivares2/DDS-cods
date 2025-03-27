from bs4 import BeautifulSoup
import requests
import csv
url = 'https://www.lanacion.com.ar/economia/jubilado-y-pobre-en-la-argentina-un-numero-que-exploto-en-los-ultimos-anos-y-que-la-politica-vuelve-nid18032025/'


response = requests.get(url)
print(response)

# Parsear el contenido HTML
soup = BeautifulSoup(response.text, 'html.parser')
#print(soup.prettify())
titulo = soup.find('h1', class_='com-title --font-primary --sixxl --font-extra')  # Ajusta según la página real de BBC
titulo = soup.title.string if soup.title else 'Sin titulo'

autor = soup.find('a', class_='link ln-link')
autor = autor.get_text(strip =True) if autor else 'autor no encontrado'

date = soup.find('time', class_='com-date --twoxs')
date = date.get_text(strip =True) if date else 'fecha no encontrado'

article_body = soup.find('div', class_='col-deskxl-10 offset-deskxl-1 col-desksm-11')
content = article_body.get_text(strip=True) if article_body else 'contenido no encontrado'

print(f"Título: {titulo}")
print(f"Autor: {autor}")
print(f"Fecha: {date}")
print(f"Contenido: {content[:200]}...") 
with open('articulo.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Título", "Autor", "Fecha", "Contenido"])
    writer.writerow([titulo, autor, date, content])

print("Artículo guardado en 'articulo.csv'")