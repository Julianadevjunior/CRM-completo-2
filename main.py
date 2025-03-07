import datetime
import streamlit as st
import requests
import pandas as pd
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import gspread
from google.oauth2.service_account import Credentials
# streamlit run main.py
st.set_page_config(layout="wide")
if "pages" not in st.session_state:
    st.session_state["pages"] = []

page_login = st.Page(page="pages/login.py", title="🧑‍ Corretor 💼")
page_cliente = st.Page(page="pages/cliente.py")
page_imovel = st.Page(page="pages/imovel.py", title="Home")
page_cadastro = st.Page(page="pages/cadastro.py")
imovel_0 = st.Page(page="pages/imovel_0.py", title="Ver mais informações")
imovel_1 = st.Page(page="pages/imovel_1.py", title="Ver mais informações")
pg = st.navigation(pages=[page_imovel, page_login, page_cliente, page_cadastro, imovel_0, imovel_1], position="hidden")

with st.sidebar:
    st.selectbox(label="▮ Tipo", options=["Apartamento", "Kitnet", "Cobertura", "Casa", "Sobrado"], label_visibility="collapsed")
    st.page_link(page_login)

st.page_link(page_imovel)


st.divider()
st.write("oi")
pg.run()
