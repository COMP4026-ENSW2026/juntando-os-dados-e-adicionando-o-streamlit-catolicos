import streamlit as st
import rafael.veneza as veneza
import rafael.adapt as adapt
import json
import pandas as pd

def get_realties():
  progress_bar = st.progress(0, f'Iniciando coleta de imóveis...')
  realty_paths = veneza.get_all_realty_paths()
  total_realties = len(realty_paths)

  progress_bar.progress(0, f'Coletando Imóveis... 0/{total_realties}')
  for c, _ in enumerate(veneza.scrape(realty_paths)):
    progress_bar.progress(c / total_realties, f'Coletando Imóveis... {c + 1}/{total_realties}')
  progress_bar.progress(1.0, f'Coleta finalizada!')
  final_realties = pd.DataFrame(adapt.adapt_realties())
  return final_realties


st.markdown("# Coleta da Imobiliária Veneza")
st.markdown('_Script do Rafael_')
st.markdown("## Progresso da Coleta")

final_realties = pd.DataFrame()
# try to open ../rafael/veneza_final.json
# if it doesn't exist, scrape the website
try:
  with open(adapt.TO_FILE, 'r', encoding='utf-8') as file:
    final_realties = pd.DataFrame(json.load(file))
  st.markdown('Dados já coletados, pulando coleta...')
  st.markdown('> Para coletar novamente, exclua o arquivo **veneza_final.json**')
except FileNotFoundError:
  final_realties = get_realties()


st.markdown('## Dados:')

st.markdown(f'- Dados coletados salvos em: **{veneza.TARGET_FILE}**')
st.markdown(f'- Dados padronizados salvos em: **{adapt.TO_FILE}**')

st.markdown('## Imóveis:')
final_realties.columns = ['URL', 'Descrição', 'Área', 'Vagas', 'Quartos', 'Preço']
final_realties['Área'] = final_realties['Área'].map(lambda x: f'{x} m²')
final_realties['Preço'] = final_realties['Preço'].map(lambda x: f'R$ {x:,.2f}')
st.dataframe(final_realties)