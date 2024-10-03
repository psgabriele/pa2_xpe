import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

password = os.getenv("senha")

# Função para conectar ao banco de dados MySQL
def conectar_ao_db():
    conexao = mysql.connector.connect(
        host="localhost",
        user="root",
        password=password,
        database="question_bank"
    )
    return conexao

