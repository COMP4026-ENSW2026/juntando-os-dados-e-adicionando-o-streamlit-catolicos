import requests
from bs4 import BeautifulSoup
import json
import streamlit as st
import pandas as pd

st.markdown("# Wesley Kasteller")
st.sidebar.markdown("# Importando dados Imobiliaria Atual")
contador = 0

lista_objetos = []
URL = 'https://www.imobiliariaatual.com.br/imoveis/apartamento-locacao'
page = requests.get(URL)

old_soup = BeautifulSoup(page.content, "html.parser")
string = old_soup.find("div", class_="list__counter").text.replace(" ", "")
max_pages = int(string.split("de")[-1])
curr_page = int(''.join(filter(str.isdigit, string.split()[0])))

total_articles = 0

while True:
  if(curr_page > max_pages):
    break

  new_url = 'https://www.imobiliariaatual.com.br/imoveis/apartamento-locacao-pagina-'+str(curr_page)
  new_page = requests.get(new_url)
  soup = BeautifulSoup(new_page.content, "html.parser")
  articles = soup.find_all("div", class_="jetgrid__col--8 jetgrid__col--sm-12 jetgrid__col--xs-24")
  total_articles += len(articles)

  curr_page += 1

print(total_articles)

curr_page = int(''.join(filter(str.isdigit, string.split()[0])))

progress_text = "Operation in progress. Please wait."
percent_complete = 0
my_bar = st.progress(0, text=progress_text)

while True:
  if(curr_page > max_pages):
    break

  new_url = 'https://www.imobiliariaatual.com.br/imoveis/apartamento-locacao-pagina-'+str(curr_page)
  new_page = requests.get(new_url)
  soup = BeautifulSoup(new_page.content, "html.parser")
  articles = soup.find_all("div", class_="jetgrid__col--8 jetgrid__col--sm-12 jetgrid__col--xs-24")

  for article in articles:
    link = "https://www.imobiliariaatual.com.br"+article.find("a", class_="list__link")["href"]
    page = requests.get(link)

    soup = BeautifulSoup(page.content, "html.parser")

    atributos = soup.find("div", class_="card__feature")

    listaAtributos = atributos.find_all("div", class_="card__item")
    if(len(listaAtributos) < 3): # Dando um break pois no anuncio em especifico não foi possível coletar os atributos
      continue

    url = link
    price = soup.find("div", class_="card__description-value").text.strip()
    for e in soup.findAll('br'):
      e.extract()
    description = soup.find("p", class_="card__text").text.strip().splitlines()[0]
    bedrooms = listaAtributos[0].find("p").text.strip()[0]
    areaString = listaAtributos[3].find("p").text.strip()
    if (areaString[2] == 'm'):
      area = areaString[0:2]
    else:
      area = areaString[0:3]
    parking = listaAtributos[2].find("p").text.strip()[0]

    if (parking == 'S'): parking = "1"
    if (parking == 'N'): parking = "0"
    if ("por" in price):
      continue
    else:
      price = price[3:]
    objeto = { "url": url, "price": float(price.replace(".", "").replace(",", ".")), "description": description, "bedrooms": int(bedrooms), "area": int(area), "parking": int(parking) }

    lista_objetos.append(objeto)

    contador += 1

  curr_page += 1
  percent_complete = int(contador / total_articles * 100) + 14
  my_bar.progress(percent_complete, text=progress_text)

percent_complete = 100
my_bar.progress(percent_complete, text=progress_text)
st.success('Imóveis coletados!')
st.markdown('')

json_file_path = './wesley/objetos.json'

df = pd.DataFrame(lista_objetos)
st.dataframe(df)
with open(json_file_path, 'w') as json_file:
  json.dump(lista_objetos, json_file, indent=2, ensure_ascii=False)