import streamlit as st
from db.avaliacao import buscar_avaliacoes, buscar_opcoes_filtro, excluir_avaliacao
from db.questao import buscar_questoes_respostas, editar_questoes_respostas

from datetime import datetime

# Verificar se há um usuário logado
if 'user_id' in st.session_state:
    user_id = st.session_state['user_id']
else:
    st.write("Nenhum usuário está logado.")

# Simulando a obtenção do ID do usuário da sessão
usuario_id = st.session_state.get('user_id', user_id) 

# Buscar opções dinâmicas para os filtros (de acordo com os valores no banco de dados)
disciplinas = ['Todas'] + buscar_opcoes_filtro('disciplina')  # Adicionar 'Todas' como opção padrão
series = ['Todas'] + buscar_opcoes_filtro('serie')
niveis = ['Todos'] + buscar_opcoes_filtro('nivel')

# Caixa de seleção para os filtros
filtro_disciplina = st.selectbox('Disciplina', disciplinas)
filtro_serie = st.selectbox('Série', series)
filtro_nivel = st.selectbox('Nível de Dificuldade', niveis)

# Campo de texto para busca por habilidade ou conteúdo
texto_busca = st.text_input('Buscar por Habilidade ou Conteúdo', placeholder="Digite parte da habilidade ou conteúdo")

# Converter 'Todas' ou 'Todos' para None
disciplina = None if filtro_disciplina == 'Todas' else filtro_disciplina
serie = None if filtro_serie == 'Todas' else filtro_serie
nivel = None if filtro_nivel == 'Todos' else filtro_nivel

# Buscar as avaliações aplicando os filtros
avaliacoes = buscar_avaliacoes(usuario_id, disciplina, serie, nivel, texto_busca)

# Exibir avaliações filtradas
if avaliacoes:
    st.write(f"Avaliações encontradas ({len(avaliacoes)}):")
    
    for avaliacao in avaliacoes:
        avaliacao_id, qnt_questao, tipo, disciplina, serie, habilidade, conteudo, nivel, created_at = avaliacao

        data_formatada = datetime.strptime(str(created_at), '%Y-%m-%d %H:%M:%S').strftime('%d/%m/%Y')
        
        # Mostrar as informações detalhadas dentro de um expander
        with st.expander(f"Avaliação de {disciplina} | {serie} | Criada em {data_formatada}"):
            st.write(f"Quantidade de Questões: {qnt_questao}")
            st.write(f"Tipo: {tipo}")
            st.write(f"Disciplina: {disciplina}")
            st.write(f"Série: {serie}")
            st.write(f"Nível: {nivel}")
            st.write(f"Conteúdo: {conteudo}")
            st.write(f"Habilidade: {habilidade}")

            # Exibir as questões e respostas associadas a essa avaliação
            questoes_respostas = buscar_questoes_respostas(avaliacao_id)
            for questao, resposta in questoes_respostas:
                st.write("### **Questões**\n")
                st.write(f"{questao}")
                st.write("### **Respostas**\n")
                st.write(f"{resposta}")
                st.write("---")

            # Exibir botões para editar ou excluir a avaliação
            col1, col2 = st.columns([1, 1])

            # Botão para excluir
            with col1:
                if st.button(f"Excluir Avaliação {avaliacao_id}"):
                    excluir_avaliacao(avaliacao_id)
                    st.success(f"Avaliação {avaliacao_id} excluída com sucesso.")
                    st.experimental_rerun()  # Atualizar a página após a exclusão

            # Botão para editar
            with col2:
                if st.button(f"Editar Avaliação {avaliacao_id}"):
                    for qr in questoes_respostas:
                        questao_texto, resposta_texto = qr

                        nova_questao = st.text_area(f"Editar Questão", value=questao_texto)
                        nova_resposta = st.text_area(f"Editar Resposta", value=resposta_texto)

                        # Salvar alterações
                        if st.button(f"Salvar alterações {avaliacao_id}"):
                            editar_questoes_respostas(nova_questao, nova_resposta)
                            st.success(f"Questão e Resposta atualizadas com sucesso!")
                            st.experimental_rerun()  # Atualiza a página após salvar

else:
    st.write("Nenhuma avaliação encontrada com os filtros selecionados.")