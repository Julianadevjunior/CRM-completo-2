import datetime
import streamlit as st
import requests
import pandas as pd
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials

col1, col2, col3 = st.columns([10, 10, 3])
with col3:
    st.page_link(label='Login',page='pages/login.py')

tamanho = 30
cor = 'red'
negrito = 'bold'
font = 'arial'
Alinhamento = 'center'
st.markdown(f"<p style='font-size:{tamanho}px; color:{cor}; font-weight:{negrito}; font-family:{font}; text-align:{Alinhamento}'>Imóvel</p>", unsafe_allow_html=True)