import requests
from bs4 import BeautifulSoup
import json

#link from the website
url_template = 'https://www.raulfulgencio.com.br/alugar/Londrina/Apartamento?pag={}'

#get number of posts from the website
response = requests.get(url_template.format(1))
soup = BeautifulSoup(response.text, 'html.parser')
quantidade = soup.find('h1', class_='titulo_res_busca')
print(quantidade.text.split()[0])