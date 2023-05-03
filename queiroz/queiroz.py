import requests
from bs4 import BeautifulSoup
import json
import re

def getInformation(page, soup, more_info):
  obj = []
  for tag in more_info:
    new_page = requests.get(tag['href'])
    new_soup = BeautifulSoup(new_page.content, "html.parser")
    title = new_soup.find("h1", class_="elementor-heading-title").text.strip()
    description = new_soup.find_all("div", class_="elementor-text-editor")
    code = description[0].findChildren()[0].text

    price_tag = new_soup.find_all("h2", class_="elementor-heading-title")
    price = ""
    for h2 in price_tag:
      if("R$" in  h2.text):
        price = float(h2.text[3:].replace('.', '').replace(',', '.'))

    text = ""
    for d in description:
      try:
        desc_text = d.find("p").text
        if("* valor aproximado" in desc_text or "Cód." in desc_text):
          continue
        else:
          text += desc_text
      except: 
        continue
    text = ' '.join([line.strip() for line in text.strip().splitlines()])

    characteristics_tag = new_soup.find_all("div", class_="property-detail")
    characteristics = ''
    for ch in characteristics_tag:
      if(len(ch)):
        for div in ch.find_all("div"):
          characteristics += div.text

    characteristics = ' '.join([line.strip() for line in characteristics.strip().splitlines()])

    properties_tag = new_soup.find_all("div", class_="property-icons-div")
    properties = ""
    for prop in properties_tag:
      for t in prop.find_all("div", class_="col-6"):
        properties += t.text

    properties = ' '.join([line.strip() for line in properties.strip().splitlines()])
    
    bedrooms_match = re.search(r'\d+ (?=Dormitórios)', properties)
    bedrooms = int(bedrooms_match.group(0)) if bedrooms_match else 0

    parking_match = re.search(r'\d+ (?=Vagas)', properties)
    parking = int(parking_match.group(0)) if parking_match else 0

    area_match = re.search(r'\d+(?=m²)', properties)
    area = int(area_match.group(0)) if area_match else 0

    if(not price):
      price = -1

    obj.append({ "url": tag['href'], "price": price, "description": text, "bedrooms": bedrooms, "area": area, "parking": parking })
  return obj  


all_pages = []
url = "https://www.imobiliariaperez.com.br/alugar/apartamento-para-alugar"
page = requests.get(url)
soup = BeautifulSoup(page.content, "html.parser")
more_info = soup.find_all("a", class_="slide-home-btn")
all_pages.append(getInformation(page, soup, more_info))
next_pages = soup.find_all("a", class_="page-link")[2:]
count = len(soup.find_all("section", class_="list-property-section")) * int(next_pages[-2].text)
print(count)

aux = next_pages[0]
i = 0
for li in next_pages:

  if(li['href'] == 'javascript:;' or li.get('aria-label') == 'pagination.next'):
    break

  next_page = requests.get(li['href'])
  next_soup = BeautifulSoup(next_page.content, "html.parser")
  next_info = next_soup.find_all("a", class_="slide-home-btn")

  all_pages.append(getInformation(next_page, next_soup, next_info))
  i += 1

json_file_path = 'objetos.json'

with open(json_file_path, 'w') as json_file:
    # Create a list to store the objects
    objects_list = []
    
    # Extract the objects from all_pages and append them to objects_list
    for page in all_pages:
        for obj in page:
            objects_list.append(obj)

    # Write the data to the JSON file
    json.dump(objects_list, json_file, indent=2, ensure_ascii=False)