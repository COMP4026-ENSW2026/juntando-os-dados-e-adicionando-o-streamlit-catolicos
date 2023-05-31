# importar dados do arquivo getDados.py

import getDados
import json

dict_list = []

for i in range(0, len(getDados.url_list)):

    dict = {
        'url': getDados.url_list[i],
        'price': float(getDados.price_list[i]),
        'description': getDados.description_list[i],
        'bedrooms': getDados.bedrooms_list[i],
        'area': int(float(getDados.area_list[i])),
        'parking': int(getDados.parking_list[i])
    }

    dict_list.append(dict)


path = "soares/Imobi.json"

with open(path, 'w', encoding='utf8') as file:
    json.dump(dict_list, file, indent=2, ensure_ascii=False)