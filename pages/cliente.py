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
import functions_sheets
# streamlit run main.py

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

lista = functions_sheets.read(pagina=1)

for linha in lista:
    nome = linha["nome"]
    telefone = linha["telefone"]
    bairro = linha["bairro"]
    valor = linha["valor"]
    descricao = linha["descriçao"]
    data_in = datetime.datetime.strptime(linha["data_in"], '%Y-%m-%d %H:%M:%S.%f')
    data_apdate = datetime.datetime.strptime(linha["data_update"], '%Y-%m-%d %H:%M:%S.%f')
    data_agenda = datetime.datetime.strptime(linha["data_agenda"], '%Y-%m-%d %H:%M:%S.%f')


    def verificar_status(data_agenda):
        agora = datetime.datetime.now()
        diferenca = agora - data_agenda  # Calcula a diferença entre o momento atual e a data agendada

        segundos_passados = diferenca.total_seconds()

        if segundos_passados > 0:  # Se já passou do horário
            if segundos_passados <= 86400:  # 86400 segundos = 1 dia
                st.write("Amarelo (passou do horário, mas menos de 24h)")
                return "🟡"
            else:
                st.write("Vermelho (passou mais de 24h)")
                return "🔴"
        else:
            st.write("Verde (ainda não chegou o horário)")
            return "🟢"


    # Exemplo de uso:
    status = verificar_status(data_agenda)


    with st.expander(label=f"{status}Nome: {nome} {'_'*(21-len(nome))} in: 📅{data_in.strftime('%d/%m/%Y %H:%M')}"):
        st.markdown(f"<p style='color:red; font-size:20px; text-align:center'><b>Bairro:</b> {bairro} ____ <b>Valor:</b> R${valor:,.2f}</p>", unsafe_allow_html=True)
        with st.container(border=True):
            st.write("Descrição")
            st.markdown(f"<p style='color:red; font-size:15px; text-align:center'>{descricao}</p>",unsafe_allow_html=True)
        st.markdown(f"<p style='color:red; font-size:12px; text-align:center'><b>Atualizado:</b> 📅{data_apdate.strftime('%d/%m/%Y %H:%M')} _____________ <b>Retornar:</b> 📅{data_agenda.strftime('%d/%m/%Y %H:%M')}</p>", unsafe_allow_html=True)

