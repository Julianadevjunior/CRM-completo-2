import datetime
import streamlit as st
import requests
import pandas as pd
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import gspread
from google.oauth2.service_account import Credentials

if "pages" not in st.session_state:
    st.session_state["pages"] = []

page_login = st.Page(page="pages/login.py")
page_cliente = st.Page(page="pages/cliente.py")
page_imovel = st.Page(page="pages/imovel.py")
page_cadastro = st.Page(page="pages/cadastro.py")
pg = st.navigation(pages=[page_imovel, page_login, page_cliente, page_cadastro])
pg.run()
