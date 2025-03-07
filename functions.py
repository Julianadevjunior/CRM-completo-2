import streamlit as st
import pandas as pd
import datetime
import time
import os
import twilio
import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from PIL import Image
from io import BytesIO

import functions_sheets

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



def cadastrar_imovel():
    def gerador_cod():
        lista_cod = []
        df_imoveis = functions_sheets.read(pagina=2)
        for cod in range(0, len(df_imoveis)):
            lista_cod.append(df_imoveis[cod]["cod"])

        cod = 0
        while True:
            if cod in lista_cod:
                cod += 1
            else:
                break
        return cod

    cod_imovel = gerador_cod()
    cod = st.text(f"Cod: {cod_imovel} ______________________{datetime.datetime.today().now().strftime("%d/%m/%Y - %H:%M")}")
    with st.container(border=True, key="container 1"):
        residencial = st.text_input(label="Residencial", key="residencial")
        complemento = st.text_input(label="Complemento", key="complemento")
        responsável = st.text_input(label="Responsável", key="resposavel")
        telefone = st.text_input(label="Telefone", key="telefone")

    with st.container(border=True, key="container 2"):
        col1, col2 = st.columns([2, 2])
        with col1:
            cep = st.text_input(label="CEP", key="cep")
            numero = st.text_input(label="N°", key="numero")
        with col2:
            mar = st.text_input(label="Distâcia do mar", key="mar")
            area = st.text_input(label="Area", key="area")

    with st.container(border=True, key="container 3"):
        quartos = st.radio(label="Quartos", options=[1, 2, 3, 4, 5], key="quartos", horizontal=True)
        vagas = st.radio(label="Vagas", options=[1, 2, 3, 4, 5], key="vagas", horizontal=True)
        banheiros = st.radio(label="Banheiros", options=[1, 2, 3, 4, 5], key="banheiros", horizontal=True)

    with st.container(border=True, key="container 4"):
        iptu = st.text_input(label="IPTU", key="iptu")
        condominio = st.text_input(label="Condominio", key="condominio")
        valor = st.text_input(label="Valor", key="valor")
        col3, col4 = st.columns([2, 2])
        with col3:
            financiamento = st.checkbox(label="Financiamento", key="financiamento")
        with col4:
            permuta = st.checkbox(label="Permuta", key="permuta")

    with st.container(border=True, key="container 5"):
        criar_pasta(f"midia_imove_{cod_imovel}")
        lista_foto = st.file_uploader(label="Fotos", accept_multiple_files=True, key="fotos")
        lista_video = st.file_uploader(label="Vídeos", accept_multiple_files=True, key="videos")
        for i, item in enumerate(lista_foto):
            img = Image.open(item)
            img.save(f"midia_imove_{cod_imovel}/fotos/img_{i}")

    descricao = st.text_area(label="Descrição", key="descricao")

    if st.button(label="Cadastrar", key="cadastrar imovel"):
        dados_imovel = [cod_imovel, residencial, complemento, responsável, telefone, cep, numero, mar, area, quartos, vagas, banheiros, iptu, condominio, valor, financiamento, permuta, descricao, str(datetime.datetime.today().now())]
        functions_sheets.create(dados_imovel, pagina=2)
        st.rerun()


def resize_image(image_path, width, height, orientation=None):
    """Redimensiona e ajusta a orientação de uma imagem."""
    try:
        img = Image.open(image_path)

        # Ajusta a orientação, se necessário
        if orientation == "horizontal":
            img = img.transpose(Image.Transpose.ROTATE_90)
        elif orientation == "vertical":
            img = img.transpose(Image.Transpose.ROTATE_270)

        # Redimensiona a imagem
        img = img.resize((width, height))

        # Salva a imagem redimensionada em um buffer de bytes
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        return buffered.getvalue()
    except Exception as e:
        print(f"Erro ao processar imagem: {e}")
        return None


def criar_pasta(pasta):
    # Verifica se a pasta já existe para não dar erro
    if not os.path.exists(pasta):
        os.mkdir(pasta)  # Cria a pasta
        os.mkdir(f"{pasta}/fotos")
        os.mkdir(f"{pasta}/videos")
        print(f"Pasta '{pasta}' criada com sucesso!")
    else:
        print(f"A pasta '{pasta}' já existe.")


# Função para salvar as imagens na pasta especificada
def salvar_imagens(imagens, pasta='midia_imovel_0', tamanho=(800, 600)):
    if not os.path.exists(pasta):
        os.makedirs(pasta)
    for imagem in imagens:
        if imagem is not None:
            caminho_completo = os.path.join(pasta, imagem.name)
            img = Image.open(imagem)
            img_resized = img.resize(tamanho)
            img_resized.save(caminho_completo)
            st.success(f"Imagem {imagem.name} salva com sucesso em {pasta}!")


def true_false(valor):
    if valor == True:
        return "Sim"
    else:
        return "Não"