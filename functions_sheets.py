import gspread
from google.oauth2.service_account import Credentials
import streamlit as st  # Ou use python-dotenv para .env


from google.oauth2 import service_account


# Carregar segredos
secrets = st.secrets["gcp_service_account"]

# Autenticação direta (sem arquivo JSON)
creds = Credentials.from_service_account_info(secrets, scopes=[
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
])

client = gspread.authorize(creds)

# Acessar planilha e aba
spreadsheet = client.open("Meu CRM Seguro")  # Nome exato da planilha!
worksheet = spreadsheet.worksheet("Página1")  # Nome da aba

# --- Operações CRUD ---
def create(data: list):
    worksheet.append_row(data)

def read():
    return worksheet.get_all_records()

def update(row: int, col: int, value: str):
    worksheet.update_cell(row, col, value)

def delete(row: int):
    worksheet.delete_rows(row)

# Exemplo de uso
create(["Julia", "maria@email.com", "Ativo"])
print(read())

