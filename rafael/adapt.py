import json
from veneza import scrape
from os import listdir, path
from sys import argv


def cast(val, type_=int, default=None):
  try:
    return type_(val)
  except ValueError:
    return default


def adapt_realty(realty):
  details = realty['details']

  new_realty = {
    'url': realty['url'],
    'description': realty['description'],
    'area': cast(details['area'].split('m2', 1)[0], int, 0),
    'parking': cast(details['parking'].split(' ', 1)[0], int, 0),
    'bedrooms': cast(details['bedrooms'].split(' ', 1)[0], int, 0),
  }

  price = realty['prices']['aluguel bruto']
  price = price.split(' ', 1)[1]
  price = price.replace('.', '').replace(',', '.')  # 1.000,00 -> 1000.00
  new_realty['price'] = float(price)

  return new_realty


if __name__ == '__main__':
  FROM_FILE = path.join(path.dirname(__file__), 'veneza.json')
  TO_FILE = path.join(path.dirname(__file__), 'veneza_final.json')

  if any([
    not 'veneza.json' in listdir(),
    len(argv) > 1 and '--scrape' in argv
  ]):
    scrape()

  with open(FROM_FILE, 'r', encoding='utf-8') as file:
    realties = json.load(file)

  adapted_realties = [adapt_realty(realty) for realty in realties]

  with open(TO_FILE, 'w') as file:
    json.dump(adapted_realties, file, indent=2, ensure_ascii=False)
  print('Dados padronizados salvos em', TO_FILE)
  print('Total de imóveis:', len(adapted_realties))