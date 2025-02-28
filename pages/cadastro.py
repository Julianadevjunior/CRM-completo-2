import datetime
import streamlit as st
import requests
import pandas as pd
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import functions
import time
import twilio

popover = st.popover(label="⋘")

with popover:
    st.page_link(label='Sair', page='pages/login.py')
    st.page_link(label='Cliente', page='pages/cliente.py')


tamanho = 30
cor = 'red'
negrito = 'bold'
font = 'arial'
Alinhamento = 'center'
st.markdown(f"<p style='font-size:{tamanho}px; color:{cor}; font-weight:{negrito}; font-family:{font}; text-align:{Alinhamento}'>Cadastros</p>", unsafe_allow_html=True)

url = st.secrets["my_secrets"]["url"]
tabela_df = st.secrets["my_secrets"]["tabela_df"]
response = requests.get(url)

tabela = {}

#Transformar o response em um dicionário tabela
for i, item in enumerate(response.json()):
    if i == 0:
        for nome in item:
             tabela[nome] = []

    else:
        for i, nome in enumerate(item):
            tabela[list(tabela.keys())[i]].append(nome)

df = pd.DataFrame(tabela)

with st.expander(label="Cadastrar cliente"):
    cod = 0
    while True:
        if cod in df["cod"].values:
            cod += 1
        else:
            break

    nome = st.text_input(label="Nome: ")
    telefone = st.text_input(label="Telefone: ")
    bairro = st.selectbox(label="Bairro", options=["Aviação", "Ocian", "Mirim"])
    valor = st.text_input(label="Valor R$: ")
    descricao = st.text_area(label="Descrição")
    data_in = datetime.datetime.today().now()
    data_update = datetime.datetime.today().now()
    data_agenda = ""
    st.write("cliente")
    lista = [cod, nome, telefone, bairro, valor, descricao, data_in, data_update, data_agenda]
    # if st.button(label="Cadastrar cliente", key="cadastrar_cliente"):
    #     functions.inserir_dados(lista)

with st.expander(label="Cadastrar Imóvel"):
    st.write("Imóvel")

