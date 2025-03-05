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


def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Substitua 'sua_imagem.jpg' pelo caminho da sua imagem
bin_str = get_base64_of_bin_file('banner.png')

st.markdown(
    f"""
    <style>
    .banner-container {{
        width: 100%;
        height: 300px;
        position: relative;
        background: url("data:image/png;base64,{bin_str}") no-repeat center top 80%;
        background-size: cover;
        display: flex;
        justify-content: center;
        align-items: center;
        color: white;
        font-size: 36px;
        font-weight: bold;
    }}
    </style>

    <div class="banner-container">
        Viver bem é morar bem!
    </div>
    """,
    unsafe_allow_html=True,
)


popover = st.popover(label="Corretor")

with popover:
    st.page_link(label='Login', page='pages/login.py')

st.divider()
pesquisa = st.selectbox(label="🔎 Pesquisar por bairro", options=["Aviação", "Ocian", "Mirim"])



df_imoveis = functions_sheets.read(pagina=2)

num_colunas = 2 # Defina o número de colunas desejado
colunas = st.columns(num_colunas)

for i, imovel in enumerate(df_imoveis):
    cod_imovel = imovel["cod"]
    valor = imovel["valor"]
    iptu = imovel["iptu"]
    condominio = imovel["condominio"]
    financiamento = imovel["financiamento"]
    permuta = imovel["permuta"]
    cep = imovel["cep"]
    bairro = requests.get(url=f"https://viacep.com.br/ws/{cep}/json/").json()["bairro"]

    valor = f"{valor:,.0f}".replace(",", ".")
    condominio = f"{condominio:,.0f}".replace(",", ".")
    iptu = f"{iptu:,.0f}".replace(",", ".")

    with colunas[i % num_colunas]: # Use o operador % para distribuir os imóveis entre as colunas
        with st.container(border=True, key=f'container_imovel{cod_imovel}'):
            resized_image = functions.resize_image(f"{i}.png", 500, 400)  # Ajuste o caminho da imagem e a orientação, se necessário
            if resized_image:
                st.image(resized_image, use_container_width=False)
            # st.image(f"{i}.png")
            st.markdown(f"""
                <div style="display: flex; justify-content: space-between;">
                    <div style="background-color: white; padding: 10px; width: 50%; font-size:28px">R$<b>{valor}</b></div>
                    <div style="background-color: white; padding: 10px; width: 50%; font-size:18px; text-align:right"><b>IPTU:</b> R${iptu}</div>
                </div>
            """, unsafe_allow_html=True)
            st.markdown(f"""
                <div style="display: flex; justify-content: space-between;">
                    <div style="background-color: white; padding: 10px; width: 50%; font-size:18px"><b>{bairro}</b></div>
                    <div style="background-color: white; padding: 10px; width: 50%; text-align:right"><b>COND:</b> R${condominio}</div>
                </div>
            """, unsafe_allow_html=True)
            st.markdown(f"""
                <div style="display: flex; justify-content: space-between;">
                    <div style="background-color: white; padding: 10px; width: 25%; font-size:18px; text-align:center"><b>🛏️{imovel["quartos"]}</b></div>
                    <div style="background-color: white; padding: 10px; width: 25%; font-size:18px; text-align:center"><b>🚽{imovel["banheiros"]}</b></div>
                    <div style="background-color: white; padding: 10px; width: 25%; font-size:18px; text-align:center"><b>🚘{imovel["vagas"]}</b></div>
                    <div style="background-color: white; padding: 10px; width: 25%; font-size:18p; text-align:center"><b>📐{imovel["area"]}</b> </div>
                </div>
            """, unsafe_allow_html=True)
            st.button(label="Ver informações", use_container_width=True, key=f"button_infsimovel_{cod_imovel}")

st.divider()
st.markdown(f"""
    <div style="display: flex; justify-content: space-between;">
        <div style="background-color: white; padding: 50px; width: 100%; font-size:15px; text-align:center">2025 Copyright - FELIPE CARLOS - CRECI 000000 -  Todos os direitos reservados</div>
    </div>
""", unsafe_allow_html=True)