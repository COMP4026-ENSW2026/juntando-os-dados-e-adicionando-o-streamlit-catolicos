import json
from bs4 import BeautifulSoup as bs
import requests
from os import path


BASE_URL = 'https://www.veneza.com.br'
BASE_RENT_URL = BASE_URL + '/imoveis/apartamento-casa-residencial-alugar-londrina'
TARGET_FILE = path.join(path.dirname(__file__), 'veneza.json')


def get_content(url):
  return bs(requests.get(url).content, 'html.parser')


def get_total_pages():
  try:
    total = get_content(BASE_RENT_URL).find('ul', class_='list__pagination')['data-total']
    return int(total)
  except ValueError | TypeError:
    return 1


def get_realty_paths(page_urls):
  paths = []
  for page_url in page_urls:
    realty_list = [item['href'] for item in get_content(page_url).find(
      'div', class_='jetgrid jetgrid--justify-left jetgrid--align-top').find_all('a', class_='list__link')]
    paths.extend(realty_list)
  return paths


def get_realty_info(realty_url):
  content = get_content(realty_url).find('section', class_='card')
  info = {
    'url': realty_url,
  }
  info['description'] = content.find('p', class_='card__text').text[:-116].strip()
  # info['imgs'] = [i['src'] for i in content.find('div', class_='card__gallery jetslider').find_all('img')]

  content_rem = content.find('div', class_='jetgrid__col--7 jetgrid__col--lg-8 jetgrid__col--md-24')

  details = bs(''.join([str(i.find('div')) for i in content_rem.find(
    'div', class_='card__background').find_all('div', class_='card__item')]), 'html.parser')

  def det_filter(i, s): return s in i.find('img')['src']
  info['details'] = {
    'area': details.find(lambda i: det_filter(i, 'img-area-size'), recursive=False),
    'parking': details.find(lambda i: det_filter(i, 'img-car'), recursive=False),
    'bedrooms': details.find(lambda i: det_filter(i, 'img-bedroom-size'), recursive=False),
  }

  for key, val in info['details'].items():
    info['details'][key] = val.text.strip() if val else '0'

  prices_container = content_rem.find('div', class_='card__total')
  price_names = prices_container.find_all('p', class_='card__total-description')
  price_vals = prices_container.find_all('p', class_='ui__text--green')

  info['prices'] = dict()
  for name, val in zip(price_names, price_vals):
    key = name.text.strip().lower()[:-1]  # termina em ':'
    info['prices'][key] = val.text.strip()

  return info


def scrape():
  print('Iniciando coleta de dados da Veneza...')
  page_links = [f'{BASE_RENT_URL}-pagina-{page}' for page in range(1, get_total_pages() + 1)]

  realty_paths = get_realty_paths(page_links)
  print(len(realty_paths))
  realties = []
  for p in realty_paths:
    try:
      realties.append(get_realty_info(BASE_URL + p))
    except Exception:
      print('\tProblema na coleta do imóvel:', BASE_URL + p)
      print('\tPulando para o próximo...')

  if len(realties) == 0:
    return

  with open(TARGET_FILE, 'w') as file:
    json.dump(realties, file, indent=2, ensure_ascii=False)
  print('Coleta finalizada! Dados salvos em', TARGET_FILE)


__all__ = ['scrape']

if __name__ == '__main__':
  scrape()