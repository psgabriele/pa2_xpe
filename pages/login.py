import streamlit as st

# Função para exibir a página de login
def login_page():
    st.title("Login")
    st.write("Por favor, insira suas credenciais para fazer login.")

    # Campos de entrada para login
    username = st.text_input("E-mail")
    password = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        # Adicionar a lógica para autenticação
        st.success(f"Bem-vindo, {username}!")
        st.session_state.logged_in = True
        st.rerun()
    
    # Link para a página de cadastro
    st.write("Não tem uma conta?")
    if st.button("Cadastre-se"):
        st.session_state.page = "register"

# Função para exibir a página de cadastro
def register_page():
    st.title("Cadastro")
    st.write("Por favor, preencha os campos para criar uma nova conta.")

    # Campos de entrada para cadastro
    username = st.text_input("E-mail", key="email")
    password = st.text_input("Senha", type="password", key="register_password")
    confirm_password = st.text_input("Confirmar Senha", type="password", key="register_confirm_password")

    if st.button("Cadastrar"):
        # Adicionar a lógica para o cadastro
        if password == confirm_password:
            st.success(f"Conta criada com sucesso para {username}!")
        else:
            st.error("As senhas não coincidem.")

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