#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import streamlit as st
from sklearn.ensemble import ExtraTreesRegressor
import joblib
import os
import requests


# === Função para baixar arquivos do Google Drive com token de confirmação ===
def download_file_from_google_drive(file_id, destination):
    URL = "https://docs.google.com/uc?export=download"
    session = requests.Session()
    response = session.get(URL, params={'id': file_id}, stream=True)

    def get_confirm_token(response):
        for key, value in response.cookies.items():
            if key.startswith('download_warning'):
                return value
        return None

    token = get_confirm_token(response)
    if token:
        params = {'id': file_id, 'confirm': token}
        response = session.get(URL, params=params, stream=True)

    with open(destination, "wb") as f:
        for chunk in response.iter_content(32768):
            if chunk:
                f.write(chunk)

# === Interface do Streamlit ===

x_numericos = {'latitude': 0, 'longitude': 0, 'accommodates': 0, 'bathrooms': 0, 'bedrooms': 0, 'beds': 0, 'extra_people': 0,
               'minimum_nights': 0, 'ano': 0, 'mes': 0, 'n_amenities': 0, 'host_listings_count': 0}

x_tf = {'host_is_superhost': 0, 'instant_bookable': 0}

x_listas = {'property_type': ['Apartment', 'Bed and breakfast', 'Condominium', 'Guest suite', 'Guesthouse', 'Hostel', 'House', 'Loft', 'Outros', 'Serviced apartment'],
            'room_type': ['Entire home/apt', 'Hotel room', 'Private room', 'Shared room'],
            'cancellation_policy': ['flexible', 'moderate', 'strict', 'strict_14_with_grace_period']
            }

dicionario = {}
for item in x_listas:
    for valor in x_listas[item]:
        dicionario[f'{item}_{valor}'] = 0
#print(dicionario)       

for item in x_numericos:
    if item == 'latitude' or item == 'longitude':
        valor = st.number_input(f'{item}', step=0.00001, value=0.0, format="%.5f")
    elif item == 'extra_people':
        valor = st.number_input(f'{item}', step=0.01, value=0.0, format="%.2f")
    else:
        valor = st.number_input(f'{item}', step=1, value=0)
    x_numericos[item] = valor
    
for item in x_tf:
    valor = st.selectbox(f'{item}', ('Sim', 'Não'))
    if valor == 'Sim':
        x_tf[item]= 1
    else:
        x_tf[item]= 0
    
for item in x_listas:
    valor = st.selectbox(f'{item}', x_listas[item])
    dicionario[f'{item}_{valor}'] = 1 
    
botao = st.button('Prever Valor do Imóvel')

if botao:
    dicionario.update(x_numericos)
    dicionario.update(x_tf)
    valores_x = pd.DataFrame(dicionario, index=[0])
    
    dados = pd.read_csv('dados.csv')
    colunas = list(dados.columns)[1:-1]
    
    valores_x = valores_x[colunas]

    # Informações do modelo
  
    file_id = "1ye3spxljaGmwRQn_qh2vufEUTWwBwplz"
    url = f"https://drive.google.com/uc?export=download&id={file_id}"  
    modelo_path = "modelo.joblib"

    st.write("🔽 Baixando o modelo do Google Drive...")

    # Tenta baixar com requests
    
    response = requests.get(url)
    if response.status_code == 200:
        with open(modelo_path, "wb") as f:
            f.write(response.content)
        st.success("✅ Download concluído com sucesso!")
    else:
        st.error("❌ Erro ao baixar o arquivo do Google Drive.")

    # Carrega o modelo, se o arquivo existir
    if os.path.exists(modelo_path):
        try:
            modelo = joblib.load(modelo_path)
            st.success("✅ Modelo carregado com sucesso!")
            preco = modelo.predict(valores_x)
            st.write(f"💰 Valor estimado do imóvel: R$ {preco[0]:,.2f}")
        except Exception as e:
            st.error(f"❌ Erro ao carregar o modelo: {e}")
    else:
        st.error("❌ O arquivo 'modelo.joblib' não foi encontrado.")
