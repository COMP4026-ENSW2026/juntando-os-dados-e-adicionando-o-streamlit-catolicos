import json
from dados_veneza import veneza

def padroniza(dados):
    objetos = []
    for d in dados:
        obj = {
            'url': d[0],
            "price": float(d[1].replace('R$ ', '').replace('.', '').replace(',', '.')),
            "description": d[2],
            "bedrooms": int(d[3][0]),
            "area": int(d[4].split('m')[0]),
            "parking": int(d[5][0])
        }
        objetos.append(obj)
    json_object = json.dumps(objetos)

    with open('dados.json', 'w') as json_file:
        json.dump(objetos, json_file, indent=2, ensure_ascii=False)

    return json_object


print(padroniza(veneza()))
