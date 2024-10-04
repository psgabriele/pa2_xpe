from db.usuarios import autenticar_usuario, criar_usuario, criar_sessao_usuario, obter_user_id
import streamlit as st
import re

# Inicializa 'user_id' se não existir na sessão
if 'user_id' not in st.session_state:
    st.session_state['user_id'] = None

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
            user_id = obter_user_id(email)
            criar_sessao_usuario(user_id, email)
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