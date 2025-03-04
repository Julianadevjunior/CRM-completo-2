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
from google.oauth2.service_account import Credentials

popover = st.popover(label="⇶")

with popover:
    st.page_link(label='Cadastros',page='pages/cadastro.py')
    st.page_link(label='Sair', page='pages/login.py')

tamanho = 30
cor = 'red'
negrito = 'bold'
font = 'arial'
Alinhamento = 'center'
st.markdown(f"<p style='font-size:{tamanho}px; color:{cor}; font-weight:{negrito}; font-family:{font}; text-align:{Alinhamento}'>Cliente</p>", unsafe_allow_html=True)

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

for idx, linha in enumerate(df.values):
    cod, nome, telefone, bairro, valor, descricao, data_in, data_update, data_agenda = list(linha)
    status = ""
    with st.expander(label=f"Nome: {nome} {'_'*(21-len(nome))} in: {functions.format_data(2, idx, coluna='data_entrada', atual=False)}"):
        st.markdown(f"<p style='color:red; font-size:20px; text-align:center'><b>Bairro:</b> {bairro} ____ <b>Valor:</b> R${valor:,.2f}</p>", unsafe_allow_html=True)
        with st.container(border=True):
            st.write("Descrição")
            st.markdown(f"<p style='color:red; font-size:15px; text-align:center'>{descricao}</p>",unsafe_allow_html=True)
        st.markdown(f"<p style='color:red; font-size:12px; text-align:center'><b>Atualizado:</b> {functions.format_data(2, idx, coluna='data_old_update', atual=False)} _____________ <b>Retornar:</b> {functions.format_data(tipo=2, item=idx, coluna='data_new_update')}</p>", unsafe_allow_html=True)

        st.write(functions.status(0))



# def cadastro():
#     cod = functions.cod()
#     nome_data = "cadastros.xlsx"
#     with st.expander(label="Cadastro🛒"):
#         data_in = datetime.datetime.today().now()
#         nova_data = data_in + datetime.timedelta(days=4)
#         st.write(nova_data)
#         st.markdown(f"<p style='font-weight:bold; font-size:40px; text-align: center'>Cadastro</p>",
#                     unsafe_allow_html=True)
#         st.markdown(
#             f"<p style='font-size:12px; text-align: center'>Cod→{cod} ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬ Data in→{data_in.strftime("%d/%m/%Y | %H:%M")}</p>",
#             unsafe_allow_html=True)
#         nome = st.text_input(label="Nome: ")
#         telefone = st.text_input(label="Telefone: ")
#         bairro = st.selectbox(label="Bairros", options=["Aviação", "Ocian", "Tupi", "Mirim", "Samambaia", "Vila Mirim"])
#         valor = st.text_input(label="Valor: ")
#         descricao = st.text_area(label="Descrição")
#
#         if st.button("Inserir ➡️", use_container_width=True):
#             in_datas = pd.read_excel("cadastros.xlsx")
#             in_datas.loc[len(in_datas)] = [cod, nome, int(telefone), bairro, int(valor), descricao, nova_data, nova_data,
#                                            data_in]
#             in_datas.to_excel(nome_data, index=False)
#             st.success("Cadastro concluido")
#             time.sleep(3)
#             st.rerun()


# def leads():
#     nome_data_cadastros = "cadastros.xlsx"
#     df_cadastros = pd.read_excel(nome_data_cadastros)
#     df_cadastros = tabela_df
#     nome_data_imoveis = "imoveis.xlsx"
#     df_imoveis = pd.read_excel(nome_data_imoveis)
#     st.divider()
#     icone = ""
#
#     st.markdown(f"<p style='font-weight:bold; font-size:30px; text-align: center'>▬▬▬▬▬▬Leads▬▬▬▬▬▬</p>",
#                 unsafe_allow_html=True)
#
#     for item in range(0, len(df_cadastros)):
#         functions.format_data(1, item)
#         if functions.alerta_horas(df_cadastros["data_new_update"][item], item) == True:
#             icone = functions.alerta_days(df_cadastros["data_old_update"][item])
#         else:
#             icone = "🔴"
#         linha_1 = len(df_cadastros["nome"][item]) + len(functions.format_telefone(df_cadastros["telefone"][item], saida=True))
#
#         with st.expander(
#                 label=f"{icone} Nome: {df_cadastros["nome"][item]} {(35-linha_1) * '▬'} Telefone: {functions.format_telefone(df_cadastros["telefone"][item], saida=True)}"):
#             st.markdown(f"<p style='font-weight:bold; font-size:25px; text-align: center'>Dados</p>",
#                         unsafe_allow_html=True)
#
#             linha_2 = len(functions.format_data_2(df=df_cadastros["data_entrada"], item=item)) + len(functions.format_data_2(df=df_cadastros["data_old_update"], item=item))
#
#             st.markdown(
#                 f"<p style='font-size:15px; text-align: center'>Data in: {functions.format_data_2(df=df_cadastros["data_entrada"], item=item)}{(40-linha_2)*"_"}Atualização: {functions.format_data_2(df=df_cadastros["data_old_update"], item=item)}</p>",
#                 unsafe_allow_html=True)
#
#             linha_3 = len(df_cadastros["bairro"][item]) + len(functions.format_valor(df_cadastros["valor"][item]))
#             st.markdown(
#                 f"<p style='font-size:15px; text-align: center'>Bairro: {df_cadastros["bairro"][item]}{(40-linha_3)*"_"}Valor: {functions.format_valor(df_cadastros["valor"][item])}</p>",
#                 unsafe_allow_html=True)
#
#             with st.container(border=True, key=f"{item}"):
#                 st.markdown(
#                     f"<p style='font-weight:bold; font-size:15px; text-align: center'>Descrição</p>",
#                     unsafe_allow_html=True)
#                 st.markdown(
#                     f"<p style='font-size:15px; text-align: center'>{df_cadastros["data_old_update"][item]}: {df_cadastros["descricao"][item]}</p>",
#                     unsafe_allow_html=True)
#
#             #___________________________________________________comparativos____________________
#             box_compativeis = []
#             for comparativo in df_imoveis[["cod", "bairro", "valor"]].values:
#                 if_1 = df_cadastros["bairro"][item]
#                 if_2 = int(df_cadastros["valor"][item])
#                 cod, bairro, valor = comparativo
#                 valor = int(valor)
#                 maxi = (if_2 + 10000)
#                 mini = (if_2 - 30000)
#                 if f"{bairro}" == if_1 and valor >= mini and valor <= maxi:
#                     box_compativeis.append(cod)
#
#             if len(box_compativeis) > 0:
#                 for box_cod in box_compativeis:
#                     st.success(f"Indicações: imóvel {box_cod}")
#             else:
#                 st.error(
#                     f"Não tem imóveis compátiveis. Capte um imóvel no bairro {df_cadastros['bairro'][item]}, com o valor de {df_cadastros['valor'][item]}")
#             #___________________________________________________Atualizar____________________
#
#             sb = st.selectbox(label="Opções⚙️", options=["Fechar", "Atualizar", "Agendar"], key=f"selecbox_{item}")
#             if sb == "Atualizar":
#                 nota = st.text_area(label="Nota", key=f"nota_{item}")
#                 if st.button(label="Atualizar", key=f"atualizar{item}"):
#                     df_cadastros.loc[item, "descricao"] = f'{df_cadastros["descricao"][item]}\n⌂{nota}'
#                     df_cadastros.loc[item, "data_old_update"] = functions.format_data(1, 2, atual=True)
#                     df_cadastros.to_excel(nome_data_cadastros, index=False)
#                     st.rerun()
#
#             elif sb == "Agendar":
#                 data = st.date_input(label="Data", key=f"data_{item}")
#                 hora = st.time_input(label="Hora", key=f"hora_{item}")
#                 d = f"{data} {hora}"
#                 hoje = datetime.datetime.today().now()
#                 agendamento = df_cadastros["data_new_update"][item]
#                 if st.button(label="Agendar", key=f"Agendar_{item}"):
#                     df_cadastros.loc[item, "data_new_update"] = d
#                     df_cadastros.to_excel(nome_data_cadastros, index=False)
#                     st.rerun()
#             alerta_dias = functions.alerta_atualizacao(item, data=True)
#             # st.write(alerta_dias)
#             if "deve entrar em contato" in str(alerta_dias):
#                 st.error(f'{str(alerta_dias)}')
#
#
# # cadastro()
# leads()
