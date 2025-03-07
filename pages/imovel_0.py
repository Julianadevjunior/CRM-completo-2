import datetime
import streamlit as st
import requests
import pandas as pd
import os
from oauth2client.service_account import ServiceAccountCredentials
import gspread
from google.oauth2.service_account import Credentials
import functions_sheets
from PIL import Image
import base64
from io import BytesIO
import functions
from streamlit_carousel import carousel
from geopy.geocoders import Nominatim

if 'check_button_fotos' not in st.session_state:
    st.session_state['check_button_fotos'] = 0

df_imoveis = functions_sheets.read(pagina=2)
url_cep = f"https://viacep.com.br/ws/{df_imoveis[0]["cep"]}/json/"
response = requests.get(url_cep)
dados = response.json()


cod = df_imoveis[0]["cod"]
imagens = os.listdir(f"midia_imovel_{cod}/fotos")
caminho_imagens = f"midia_imovel_{cod}/fotos"
valor = df_imoveis[cod]["valor"]
quarto = df_imoveis[cod]["quartos"]
vaga = df_imoveis[cod]["vagas"]
area = df_imoveis[cod]["area"]
iptu = df_imoveis[cod]["iptu"]
condominio = df_imoveis[cod]["condominio"]
financiamento = df_imoveis[cod]["financiamento"]
permuta = df_imoveis[cod]["permuta"]
description = df_imoveis[cod]["descricao"]
bairro = dados["bairro"]

st.markdown(f"<p style='font-size:25px'>Localizado no bairro <b>{bairro}.</b></p>",
            unsafe_allow_html=True)
num_colunas = 3 # Defina o número de colunas desejado
colunas = st.columns(num_colunas)

for i, imagem in enumerate(imagens):
    with colunas[i % num_colunas]:
        st.image(f"{caminho_imagens}/{imagem}")
        st.write(imagem)
    if i == 2:
        break


bto_fotos = st.button("Todas as imagens", use_container_width=True)

if bto_fotos:
    st.session_state['check_button_fotos'] += 1

if bto_fotos and st.session_state['check_button_fotos'] == 1:
    for i, imagem in enumerate(imagens[3:]):
        with colunas[i % num_colunas]:
            st.image(f"{caminho_imagens}/{imagem}")
            st.write(imagem)

if st.session_state['check_button_fotos'] >=2:
    st.session_state['check_button_fotos'] = 0


col1, col2, col3, col4, col5 = st.columns([5, 4, 3, 3, 3])

with col1:
    st.markdown(f"<p style='font-size:25px'><b>{functions.format_valor(valor)}</b>/Venda</p>", unsafe_allow_html=True)

    with st.container(border=True, key='valores'):
        st.markdown(f"<p style='font-size:15px'>→Cond.: <b>{functions.format_valor(condominio)}</b></p>",
                    unsafe_allow_html=True)
        st.markdown(f"<p style='font-size:15px'>→IPTU: <b>{functions.format_valor(iptu)}</b></p>",
                    unsafe_allow_html=True)
        st.markdown(f"<p style='font-size:15px'>→Permuta: <b>{functions.true_false(permuta)}</b></p>",
                    unsafe_allow_html=True)
        st.markdown(f"<p style='font-size:15px'>→Financiamento: <b>{functions.true_false(financiamento)}</b></p>",
                    unsafe_allow_html=True)

with col3:
    st.markdown(f"<p style='font-size:30px'><b>🛏️</b></p><p style='font-size:20px'><b>{quarto}</b> quarto(s)</p>", unsafe_allow_html=True)
with col4:
    st.markdown(f"<p style='font-size:30px'><b>🚘</b></p><p style='font-size:20px'><b>{vaga}</b> vaga(s)</p>", unsafe_allow_html=True)
with col5:
    st.markdown(f"<p style='font-size:30px'><b>📐</b></p><p style='font-size:20px'><b>{area}</b>m²</p>", unsafe_allow_html=True)

with st.container(border=True, key='descrição'):
    st.markdown(f"<p style='font-size:18px'><b>Descrição</b></p>",
                unsafe_allow_html=True)
    st.markdown(f"<p style='font-size:15px'>{description}</p>",
                unsafe_allow_html=True)

def location(cep):
    url_cep = f"https://viacep.com.br/ws/{cep}/json/"
    response = requests.get(url_cep)
    dados = response.json()

    # Inicializa o geocodificador com um user_agent personalizado (obrigatório)
    geolocator = Nominatim(user_agent="my_app")

    # Insira o endereço desejado
    endereco = f"{dados['logradouro']}, 477, {dados['localidade']}, Brasil"

    localizacao = geolocator.geocode(endereco)
    lat = localizacao.latitude
    lon = localizacao.longitude
    return {"LAT": [lat], "LON": [lon]}

st.map(location(df_imoveis[cod]["cep"]), size=100, zoom=14)

st.divider()
st.markdown(f"""
    <div style="display: flex; justify-content: space-between;">
        <div style="background-color: white; padding: 50px; width: 100%; font-size:15px; text-align:center">2025 Copyright - FELIPE CARLOS - CRECI 000000 -  Todos os direitos reservados</div>
    </div>
""", unsafe_allow_html=True)