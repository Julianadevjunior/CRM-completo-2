import datetime
import streamlit as st
import requests
import pandas as pd
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import gspread
from google.oauth2.service_account import Credentials


popover = st.popover(label="⇶")

with popover:
    st.page_link(label='Login', page='pages/login.py')

tamanho = 30
cor = 'red'
negrito = 'bold'
font = 'arial'
Alinhamento = 'center'
st.markdown(f"<p style='font-size:{tamanho}px; color:{cor}; font-weight:{negrito}; font-family:{font}; text-align:{Alinhamento}'>Imóvel</p>", unsafe_allow_html=True)