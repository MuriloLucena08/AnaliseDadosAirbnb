import pandas as pd
import streamlit as st
from sklearn.ensemble import ExtraTreesRegressor
import joblib
import os
import requests

# === Função para baixar modelo do S3 ===
def baixar_modelo_do_s3(url, destino):
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(destino, 'wb') as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            return True
        else:
            return False
    except Exception as e:
        st.error(f"Erro ao baixar modelo do S3: {e}")
        return False

# === Interface do Streamlit ===

x_numericos = {
    'latitude': 0, 'longitude': 0, 'accommodates': 0, 'bathrooms': 0,
    'bedrooms': 0, 'beds': 0, 'extra_people': 0, 'minimum_nights': 0,
    'ano': 0, 'mes': 0, 'n_amenities': 0, 'host_listings_count': 0
}

x_tf = {'host_is_superhost': 0, 'instant_bookable': 0}

x_listas = {
    'property_type': [
        'Apartment', 'Bed and breakfast', 'Condominium', 'Guest suite',
        'Guesthouse', 'Hostel', 'House', 'Loft', 'Outros', 'Serviced apartment'
    ],
    'room_type': [
        'Entire home/apt', 'Hotel room', 'Private room', 'Shared room'
    ],
    'cancellation_policy': [
        'flexible', 'moderate', 'strict', 'strict_14_with_grace_period'
    ]
}

dicionario = {}
for item in x_listas:
    for valor in x_listas[item]:
        dicionario[f'{item}_{valor}'] = 0

for item in x_numericos:
    if item in ['latitude', 'longitude']:
        valor = st.number_input(f'{item}', step=0.00001, value=0.0, format="%.5f")
    elif item == 'extra_people':
        valor = st.number_input(f'{item}', step=0.01, value=0.0, format="%.2f")
    else:
        valor = st.number_input(f'{item}', step=1, value=0)
    x_numericos[item] = valor

for item in x_tf:
    valor = st.selectbox(f'{item}', ('Sim', 'Não'))
    x_tf[item] = 1 if valor == 'Sim' else 0

for item in x_listas:
    valor = st.selectbox(f'{item}', x_listas[item])
    dicionario[f'{item}_{valor}'] = 1

botao = st.button('Prever Valor do Imóvel')

if botao:
    st.write("✅ Botão clicado")
    dicionario.update(x_numericos)
    dicionario.update(x_tf)
    valores_x = pd.DataFrame(dicionario, index=[0])
    st.write("🔎 Shape do input:", valores_x.shape)

    try:
        dados = pd.read_csv('dados.csv')
        st.write("📄 'dados.csv' carregado com sucesso")
        colunas = list(dados.columns)[1:-1]
        valores_x = valores_x[colunas]
    except Exception as e:
        st.error(f"❌ Erro ao ler 'dados.csv': {e}")
        st.stop()

    modelo_path = "modelo.joblib"
    modelo_url = "https://meu-bucket-streamli-joblib.s3.us-east-2.amazonaws.com/modelo.joblib"

    if not os.path.exists(modelo_path):
        st.info("🔄 Baixando o modelo do S3...")
        sucesso = baixar_modelo_do_s3(modelo_url, modelo_path)
        if not sucesso:
            st.error("❌ Falha ao baixar o modelo do S3.")
            st.stop()
        else:
            st.write("📥 Modelo baixado. Tamanho:", os.path.getsize(modelo_path))

    try:
        modelo = joblib.load(modelo_path)
        st.success("✅ Modelo carregado com sucesso!")
        st.write("⚙️ Realizando predição...")
        preco = modelo.predict(valores_x)
        st.write(f"💰 Valor previsto: R$ {preco[0]:,.2f}")
    except Exception as e:
        st.error(f"❌ Erro ao carregar ou prever com o modelo: {e}")
