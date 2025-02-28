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

col1, col2, col3 = st.columns([10, 10, 3])
with col3:
    st.page_link(label='Voltar',page='pages/imovel.py')

tamanho = 30
cor = 'red'
negrito = 'bold'
font = 'arial'
Alinhamento = 'center'
st.markdown(f"<p style='font-size:{tamanho}px; color:{cor}; font-weight:{negrito}; font-family:{font}; text-align:{Alinhamento}'>Login</p>", unsafe_allow_html=True)


with st.container(border=True, key="container_login"):
    email = st.text_input(label="E-mail", placeholder="Insira o seu e-mail")
    senha = st.text_input(label="Senha", placeholder="Insira a sua senha")
    if st.button(label="Confirmar") and email == st.secrets["my_secrets"]["email"] and senha == st.secrets["my_secrets"]["senha"]:
        st.page_link(label='Entrar', page='pages/cliente.py')
