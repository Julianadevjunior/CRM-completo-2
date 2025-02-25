import datetime
import streamlit as st
import requests
import pandas as pd
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials

if "pages" not in st.session_state:
    st.session_state["pages"] = []

page_login = st.Page(page="pages/login.py")
page_cliente = st.Page(page="pages/cliente.py")
page_imovel = st.Page(page="pages/imovel.py")
pg = st.navigation(pages=[page_imovel, page_login, page_cliente])
pg.run()

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

def procurar_lead(code):
    keys = ['cod',
            'nome',
            'telefone',
            'bairro',
            'valor',
            'descricao',
            'data_entrada',
            'data_old_update',
            'data_new_update']

    lista_dados = []
    for idx, cod in enumerate(df['cod'].values):
        if cod == code:
            for item in df.loc[idx].values:
                lista_dados.append(item)
    return lista_dados


def inserir_dados(lista):
    """

    :param lista: a lista deve conter
    [nome,
    telefone,
    bairro,
    valor,
    descricao,
    data_in,
    data_update,
    data_agenda]
    :return:
    """
    # Configurações de acesso
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(f"{tabela_df}", scope)
    client = gspread.authorize(creds)

    # Acessa a planilha
    spreadsheet = client.open("tabela cliente sheet")
    sheet = spreadsheet.sheet1  # Ou nome da aba: spreadsheet.worksheet("Nome da aba")

    # Adiciona uma linha
    nova_linha = lista
    sheet.append_row(nova_linha)

    print("Informação adicionada com sucesso!")

#Código do cliente
cod = 0
while True:
    if cod in df["cod"].values:
        cod += 1
    else:
        break

lista = [cod, 'Leonardo', '11998548715', 'Mirim', '425000', 'Com piscina',
         f"{datetime.datetime.today().now()}", f"{datetime.datetime.today().now()}",
         f"{datetime.datetime.today().now()}"]
# inserir_dados(lista)


st.dataframe(df)



