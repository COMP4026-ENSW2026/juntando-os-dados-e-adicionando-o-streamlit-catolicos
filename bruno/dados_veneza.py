import requests
from bs4 import BeautifulSoup
import streamlit as st

def veneza():
    progress_text = "Operation in progress. Please wait."
    progresso = 0
    my_bar = st.progress(progresso, text=progress_text)
    
    url = "https://www.veneza.com.br/imoveis/casa-residencial-apartamento-em-condominio-venda"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    imoveis = soup.find_all('div', class_='list__hover')
    obj_list = []

    qtd = len(imoveis)

    for i in imoveis:
        endereco = i.find('p', class_='list__address').text.strip()
        condominio = i.find('p', class_='list__building').text.strip()

        a_tag = i.find('a', class_='list__link', href=True)
        link = 'https://www.veneza.com.br' + a_tag['href']

        quartos = area = vagas = 0
        imovel_page = requests.get(link)
        imovel_soup = BeautifulSoup(imovel_page.content, "html.parser")
        dados = imovel_soup.find_all('div', class_='card__item')
        for d in dados:
            texto = d.text.strip()
            if 'quarto' in texto:
                quartos = texto.replace('                                                                ', ' ')
            if 'total' in texto:
                area = texto
            if 'vaga' in texto:
                vagas = texto

        valor = imovel_soup.find('div', class_='card__total-value').text.strip()

        descricao = imovel_soup.find('p', class_='card__text').text.strip()

        progresso += (1/qtd) * 100
        my_bar.progress(progresso)

        yield link, valor, descricao, quartos, area, vagas