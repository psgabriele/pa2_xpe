import streamlit as st
import mysql.connector
from dotenv import load_dotenv
import os
import re
import bcrypt

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

# Função para validar o formato de e-mail
def email_valido(email):
    padrao = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(padrao, email) is not None

# Função para validar a senha
def senha_valida(senha):
    if len(senha) < 8:
        return False
    if not re.search(r'[A-Za-z]', senha): # Verifica se tem letras
        return False
    if not re.search(r'[0-9]', senha): # Verifica se tem números
        return False
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', senha): # Verifica se tem caracteres especiais
        return False
    return True

# Função para buscar o hash da senha armazenada no banco de dados
def buscar_hash(email):
    conexao = conectar_ao_db()
    cursor = conexao.cursor()

    # Verifica se o usuário existe no banco de dados
    query = 'SELECT senha FROM usuarios WHERE email = %s'
    cursor.execute(query, (email,))
    resultado = cursor.fetchone()

    cursor.close()
    conexao.close()

    if resultado:
        return resultado[0] # Retorna o hash da senha
    else:
        return None

# Função para verificar se o usuário existe e validar a senha
def autenticar_usuario(email, senha):
    # Buscar o hash da senha no banco de dados
    hash_armazenado = buscar_hash(email)

    if hash_armazenado:
        # Comparar a senha fornecida com o hash armazenado
        if bcrypt.checkpw(senha.encode('utf-8'), hash_armazenado.encode('utf-8')):
            return True
        else:
            return False
    else:
        return False

# Função para criar um novo usuário no banco de dados
def criar_usuario(email, senha):
    conexao = conectar_ao_db()
    cursor = conexao.cursor()

    # Criptografar a senha antes de armazenar
    senha_criptografada = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())

    # Insere o novo usuário no banco de dados
    query = 'INSERT INTO usuarios (email, senha) VALUES (%s, %s)'
    cursor.execute(query, (email, senha_criptografada))

    conexao.commit()
    cursor.close()
    conexao.close()

# Função para exibir a página de login
def login_page():
    st.title("Login")
    st.write("Por favor, insira suas credenciais para fazer login.")

    # Campos de entrada para login
    email = st.text_input("E-mail")
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        # Autentica o usuário
        if autenticar_usuario(email, senha):
            st.success(f"Bem-vindo, {email}!")
            st.session_state.logged_in = True
            #st.rerun()
        else:
            st.error("E-mail ou senha incorretos.")
    
    # Link para a página de cadastro
    st.write("Não tem uma conta?")
    if st.button("Cadastre-se"):
        st.session_state.page = "register"

# Função para exibir a página de cadastro
def register_page():
    st.title("Cadastro")
    st.write("Por favor, preencha os campos para criar uma nova conta.")

    # Campos de entrada para cadastro
    email = st.text_input("E-mail", key="email")
    senha = st.text_input("Senha", type="password", key="register_password")
    confirmar_senha = st.text_input("Confirmar Senha", type="password", key="register_confirm_password")

    if st.button("Cadastrar"):
        # Validação da senha
        if not senha_valida(senha):
            st.error("A senha deve ter pelo menos 8 caracteres, incluindo letras, números e caracteres especiais.")
            return
        
        if senha != confirmar_senha:
            st.error("As senhas não coincidem.")
            return
        
        # Validação do email
        if email and not email_valido(email):
            st.error("O formato do e-mail é inválido.")
            return
        
        # Se tudo estiver válido, cria o usuário
        try:
            criar_usuario(email, senha)
            st.success(f"Conta criada com sucesso para {email}!")
            st.session_state.page = "login"
        except Exception as e:
                st.error(f"Erro ao criar conta: {e}")

    # Link para a página de login
    st.write("Já tem uma conta?")
    if st.button("Faça login"):
        st.session_state.page = "login"

# Função principal que controla a navegação entre páginas
def main():
    # Definir a página inicial como "login" se não estiver definida
    if 'page' not in st.session_state:
        st.session_state.page = "login"

    # Navegação entre páginas com base no estado
    if st.session_state.page == "login":
        login_page()
    elif st.session_state.page == "register":
        register_page()

# Executar a função principal
main()