import streamlit as st
import pandas as pd
import datetime
import time
import os
import twilio
import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials

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

df_cadastros = pd.DataFrame(tabela)


def dicts_teste(item):
    dict_1 = {
        "cod": [1, 2, 3, 4, 5, 6],
        "nome": ["Ana Julia", "João Pedro", "Maria Fernanda", "Carlos Eduardo",
                 "Juliana Santos", "Ricardo Oliveira"],
        "telefone": ["11998654521", "11987654321", "11976543210",
                     "11965432109", "11954321098", "11943210987"],
        "bairro": ["Aviação", "Ocian", "Tupi", "Mirim", "Samambaia",
                   "Vila Mirim"],
        "valor": ["350000", "420000", "280000", "500000", "320000", "450000"],
        "descricao": ["Com entrada parcelada", "Condomínio fechado com piscina",
                      "Próximo à orla da praia", "Novo na planta com subsolo",
                      "Chave na mão com reforma recente", "Vista para o mar"],
        "data_entrada": [datetime.datetime.now(), datetime.datetime.now(),
                         datetime.datetime.now(), datetime.datetime.now(),
                         datetime.datetime.now(), datetime.datetime.now()],
        "data_old_update": [datetime.datetime.now(), datetime.datetime.now(),
                         datetime.datetime.now(), datetime.datetime.now(),
                         datetime.datetime.now(), datetime.datetime.now()],
        "data_new_update": [datetime.datetime.now(), datetime.datetime.now(),
                            datetime.datetime.now(), datetime.datetime.now(),
                            datetime.datetime.now(), datetime.datetime.now()]
    }


    dict_2 = {
        "cod": [7, 8, 9, 10, 11],
        "nome": [
            "Mariana Costa",
            "Felipe Rocha",
            "Larissa Martins",
            "Gabriel Lima",
            "Beatriz Nogueira"
        ],
        "telefone": [
            "11991234567",
            "11992345678",
            "11993456789",
            "11994567890",
            "11995678901"
        ],
        "bairro": [
            "Canto do Forte",
            "Sítio do Campo",
            "Boqueirão",
            "Guilhermina",
            "Antártica"
        ],
        "valor": [
            "475000",
            "320000",
            "410000",
            "285000",
            "530000"
        ],
        "descricao": [
            "Cobertura duplex com varanda gourmet",
            "Casa térrea com quintal amplo",
            "Apartamento frente ao mar",
            "Sobrado em condomínio tranquilo",
            "Kitnet mobiliado próximo à praia"
        ],
        "financiamento": [True, False, True, False, True],
        "permuta": [False, True, False, True, False],
        "fotos": [
            ["imovel7_1.jpg", "imovel7_2.jpg", "imovel7_3.jpg"],
            ["casa8.jpg", "casa8_quintal.jpg"],
            ["apto9_vista.jpg", "apto9_sala.jpg", "apto9_varanda.jpg"],
            ["sobrado10_frente.jpg"],
            ["kitnet11_1.jpg", "kitnet11_2.jpg"]
        ],
        "video": [
            "tour_imovel7.mp4",
            "video_casa8.mp4",
            "apto9_video.mp4",
            "sobrado10_tour.mp4",
            "tour_kitnet11.mp4"
        ],
        "data_entrada": [datetime.datetime.now(), datetime.datetime.now(),
                         datetime.datetime.now(), datetime.datetime.now(),
                         datetime.datetime.now()],
        "data_update": [datetime.datetime.now(), datetime.datetime.now(),
                         datetime.datetime.now(), datetime.datetime.now(),
                         datetime.datetime.now()]}

    if item == 1:
        return dict_1
    if item == 2:
        return dict_2



def format_data(tipo, item, coluna, atual=False):
    data_df = tabela[f"{coluna}"][item]
    if atual == True:
        data_df = datetime.datetime.today().now()

    data_df = str(data_df)
    format_data_df = {"ano": int(data_df[:4]),
                      "mes": int(data_df[5:7]),
                      "dia": int(data_df[8:10]),
                      "hora": int(data_df[11:13]),
                      "minuto": int(data_df[14:16])}
    format_0 = datetime.datetime(format_data_df["ano"], format_data_df["mes"], format_data_df["dia"],
                                 format_data_df["hora"], format_data_df["minuto"])

    format_1 = datetime.datetime(format_data_df["ano"], format_data_df["mes"], format_data_df["dia"],
                                 format_data_df["hora"], format_data_df["minuto"]).strftime("%d/%m/%Y - %H:%M:%S")

    if tipo == 1:
        return format_0
    if tipo == 2:
        return format_1


def alerta_atualizacao(item, data=False, icone=False):
    data_1 = format_data(1, item)
    data_2 = format_data(1, 1)
    data_3 = format_data(1, 2, atual=True)

    # Calcule a diferença entre as duas datas
    diferenca = data_3 - data_1  # Ou data_2 - data_3 dependendo da ordem desejada

    # Extraia dias, horas e minutos
    dias = int(diferenca.days)
    segundos_restantes = diferenca.seconds
    horas = segundos_restantes // 3600
    minutos = (segundos_restantes % 3600) // 60

    if dias > 4:
        if data == True:
            return "Você deve entrar em contato com esse lead"
        if icone == True:
            return "🔴"
    if dias < 4 and icone == True:
        return "🟢"


def alerta_days(data):
    hoje = datetime.datetime.today().now()
    data_df = f"{data}"
    format_data_df = {"ano": int(data_df[:4]),
                      "mes": int(data_df[5:7]),
                      "dia": int(data_df[8:10]),
                      "hora": int(data_df[11:13]),
                      "minuto": int(data_df[14:16])}
    format_0 = datetime.datetime(format_data_df["ano"], format_data_df["mes"], format_data_df["dia"],
                                 format_data_df["hora"], format_data_df["minuto"])

    # Calcule a diferença entre as duas datas
    diferenca = hoje - format_0  # Ou data_2 - data_3 dependendo da ordem desejada

    # Extraia dias, horas e minutos
    dias = int(diferenca.days)
    segundos_restantes = diferenca.seconds
    horas = segundos_restantes // 3600
    minutos = (segundos_restantes % 3600) // 60
    if dias > 4:
        return "🔴"
    elif dias < 4 and dias > 2:
        return "🟡"
    else:
        return "🟢"

def alerta_horas(df, item):
    hoje = datetime.datetime.today().now()
    data_df = f"{df}"
    format_data_df = {"ano": int(data_df[:4]),
                      "mes": int(data_df[5:7]),
                      "dia": int(data_df[8:10]),
                      "hora": int(data_df[11:13]),
                      "minuto": int(data_df[14:16])}
    format_0 = datetime.datetime(format_data_df["ano"], format_data_df["mes"], format_data_df["dia"],
                                 format_data_df["hora"], format_data_df["minuto"])

    # Calcule a diferença entre as duas datas
    diferenca = format_0 - hoje # Ou data_2 - data_3 dependendo da ordem desejada

    # Extraia dias, horas e minutos
    dias = int(diferenca.days)
    segundos_restantes = diferenca.seconds
    horas = segundos_restantes // 3600
    minutos = (segundos_restantes % 3600) // 60
    if dias < 0 or horas < 0 or minutos < 0:
        return False
    else:
        return True


def format_data_2(df, item):
    data_str = f"{df[item]}"
    data_formatada = datetime.datetime.strptime(data_str, "%Y-%m-%d %H:%M:%S").strftime("%d/%m/%Y")

    return data_formatada


def format_telefone(telefone, saida=False):
    telefone = str(telefone)
    for item in telefone:
        if item.isnumeric() == False:
            telefone = item.replace(item, "")
    if saida == True:
        if telefone[:2] == '55':
            telefone = telefone[2:]

        if len(telefone) > 11:
            telefone = telefone
        else:
            if len(telefone) == 11:
                telefone = f"({telefone[:2]}){telefone[2:7]}-{telefone[7:]}"
            elif len(telefone) == 10:
                telefone = f"({telefone[:2]}){telefone[2:6]}-{telefone[6:]}"

            else:
                telefone = telefone
    return telefone


def format_valor(valor):
    valor = f"R${float(valor):,.2f}"
    if ',' in valor:
        valor = valor.replace(',', '-')
    if '.' in valor:
        valor = valor.replace('.', ',')
    if '-' in valor:
        valor = valor.replace('-', '.')

    return valor


def status(data):
    data_1 = datetime.datetime.today().now()
    data_2 = df_cadastros['data_new_update'][0]
    st.write(data_1, data_2)

    if data >= 4:
        return "🔴"
    if data <= 3 and data >= 1:
        return "🟡"
    if data < 1:
        return "🟢"

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


