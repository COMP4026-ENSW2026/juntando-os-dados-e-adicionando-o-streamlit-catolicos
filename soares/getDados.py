import requests
from bs4 import BeautifulSoup
import json
import streamlit as st

url_template = 'https://www.raulfulgencio.com.br/alugar/Londrina/Apartamento?pag={}'

# dict_list = []
url_list = []
price_list = []
description_list = []
bedrooms_list = []
area_list = []
parking_list = []
contador = 0
loop = 0

#get number of posts from the website

response = requests.get(url_template.format(1))
soup = BeautifulSoup(response.text, 'html.parser')
quantidade = soup.find('h1', class_='titulo_res_busca')
# print(quantidade.text.split()[0])

progress_text = "Coletando Imóveis. Por favor aguarde."
percent_complete = 0
my_bar = st.progress(0, text=progress_text)

for page in range(1, 4):
    url = url_template.format(page)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    posts = soup.find_all('div', class_='item col-sm-6 col-md-4 col-lg-3')

    for post in posts:
        imovel = post.find('div', class_='info')
        link = imovel.find('a')['href']
        # print(link)

        link_response = requests.get('https://www.raulfulgencio.com.br/' + link, timeout=15)
        link_soup = BeautifulSoup(link_response.text, 'html.parser')

        # percent_complete += 1
        
        try :
            prices = link_soup.find_all('div', class_='col-lg-6 col-sm-6 text-right')[-1]
            prices = prices.text.strip()
            preco_str = prices.replace("R$", "").replace(" ", "").replace(".", "").replace(",", ".")
            # print(float(preco_str))
            # preco_str = preco_str.replace(".", "").replace(",", ".")
            # print(prices)
            # price_sem_virgula = prices.text.strip().replace(',', '') # substitui a vírgula por ponto
            # prince_sem_ponto = price_sem_virgula.replace('.', '') # substitui o ponto por nada
            # print('Preço: R$', price_sem_virgula)
            # print('Preço: R$', float(price_sem_virgula))
            # url - String (Link do anúncio)
            # print('Link: ', link_response.url)
            # price - Float (preço do imóvel no anúncio)
            # print('Preço: R$', float(prince_sem_ponto))
        except IndexError:
            continue
        
        # description - String (descrição do anúncio contendo mais detalhes)
        description = link_soup.find('p', {'id': 'descricao_imovel'}).text.strip()
        # print('Descrição: ', description)

        data = link_soup.find('div', class_='main col-sm-8')

        # bedrooms - Int (quantidade de quartos no imóvel)
        condition = data.find_all('div', class_='text-center') 

        if len(condition) == 7:
            bedrooms = data.find_all('div', class_='text-center')[2]
            suites = data.find_all('div', class_='text-center')[3]
            quartos = int(bedrooms.text.split()[1]) + int(suites.text.split()[1])
        else:
            bedrooms = data.find_all('div', class_='text-center')[2]
            quartos = int(bedrooms.text.split()[1])
            # print('Quartos: ', int(bedrooms.text.split()[1]))

        # area - Int (área do imóvel em m^2)
        if len(condition) == 7:
            area = data.find_all('div', class_='text-center')[6]
            area_sem_ponto = area.text.split()[2] # substitui o ponto por nada
            # print('Área: ', int(area_sem_ponto), 'm²')
        elif len(condition) == 5:
            area = data.find_all('div', class_='text-center')[4]
            area_sem_ponto = area.text.split()[2].replace('.', '')
        else:
            area = data.find_all('div', class_='text-center')[5]
            area_sem_ponto = area.text.split()[2].replace('.', '') # substitui o ponto por nada
            # print('Área: ', int(area_sem_ponto), 'm²')

        # parking - Int (quantidade de vagas no estacionamento do imóvel)
        if len(condition) == 7:
            parking = data.find_all('div', class_='text-center')[5]
            parking = parking.text.split()[1]
        elif len(condition) == 5:
            parking = '0'
            # print('Vagas: ', int(parking.text.split()[1]))
        else:
            parking = data.find_all('div', class_='text-center')[4]
            parking = parking.text.split()[1]
            # print('Vagas: ', int(parking.text.split()[1]))

        
        url_list.append(link_response.url)
        price_list.append(preco_str)
        description_list.append(description)
        bedrooms_list.append(quartos)
        area_list.append(area_sem_ponto)
        parking_list.append(parking)

        contador += 1
    loop += 1
    
    percent_complete = int(contador / int(quantidade.text.split()[0]) * 100)

    if loop == 3 and percent_complete == 100:
        pass
    elif loop == 3 and percent_complete > 100:
        while percent_complete > 100:
            percent_complete -= 1
        pass
    elif loop == 3 and percent_complete < 100:
        while percent_complete < 100:
            percent_complete += 1
        pass
    else:
        pass

    print(percent_complete)
    my_bar.progress(percent_complete , text=progress_text)
    
    if percent_complete == 100:
        st.success('Imóveis coletados!')