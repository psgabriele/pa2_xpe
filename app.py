import streamlit as st

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login():
    st.write("Entrar")
    if st.button("Entrar"):
        st.session_state.logged_in = True
        st.rerun()

def logout():
    if st.button("Sair"):
        st.session_state.logged_in = False
        st.rerun()

login_page = st.Page("pages/login.py", title="Entrar", icon=":material/login:")
logout_page = st.Page(logout, title="Sair", icon=":material/logout:")

criar_questoes = st.Page(
    "menu/criar_questoes.py", title="Criar Questões", icon=":material/edit_square:", default=True
)
banco_de_questoes = st.Page("menu/banco_de_questoes.py", title="Banco de Questões", icon=":material/view_list:")
avaliacoes = st.Page(
    "menu/avaliacoes.py", title="Avaliações", icon=":material/checklist:"
)

perfil = st.Page("configuracoes/perfil.py", title="Perfil", icon=":material/person:")
ajuda = st.Page("configuracoes/ajuda.py", title="Ajuda", icon=":material/help:")

if st.session_state.logged_in:
    pg = st.navigation(
        {
            "Conta": [logout_page],
            "Menu": [criar_questoes, banco_de_questoes, avaliacoes],
            "Configurações": [perfil, ajuda],
        }
    )
else:
    pg = st.navigation([login_page])

pg.run()