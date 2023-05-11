import requests
from bs4 import BeautifulSoup
import json

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