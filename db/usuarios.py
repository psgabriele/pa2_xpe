from db.conexao import conectar_ao_db
import streamlit as st
import bcrypt

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
    
def obter_user_id(email):
    """
    Função que retorna o ID do usuário com base no e-mail.
    """
    conexao = conectar_ao_db()
    cursor = conexao.cursor()

    query = "SELECT id FROM usuarios WHERE email = %s"
    cursor.execute(query, (email,))
    resultado = cursor.fetchone()

    if resultado:
        return resultado[0]  # Retorna o user_id
    else:
        return None

# Função para criar uma sessão do usuário logado
def criar_sessao_usuario(user_id, user_email):
    st.session_state['user_id'] = user_id
    st.session_state['user_email'] = user_email

# Função para verificar se o usuário está logado
def verificar_sessao():
    return 'user_id' in st.session_state

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