from dotenv import load_dotenv
import os
import sys
from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import GoogleGenerativeAI
from langchain.schema import StrOutputParser
import streamlit as st

load_dotenv()

chave_api = os.getenv("GOOGLE_API_KEY")

os.environ['PYTHONIOENCODING'] = 'utf-8'
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

def criar_template_do_prompt_1():

    template = """
    Você é um professor especialista em criar questões em todos os campos de conhecimento.
    Pense passo a passo e elabore uma avaliação com {quantidade} questões do tipo {tipo}, da disciplina {disciplina},
    para alunos do {serie}, sobre o conteúdo {conteudo} e/ou competência/habilidade {habilidade} da BNCC e com nível de dificuldade {dificuldade}.

    O formato das questões é um dos seguintes:
    - Múltipla Escolha:
        Cada alternativa deve estar em uma linha separada.
    - Questões:
        Questão 1: 
            a. Resposta 1

            b. Resposta 2

            c. Resposta 3

            d. Resposta 4
        Questão 2: 
            a. Resposta 1

            b. Resposta 2

            c. Resposta 3

            d. Resposta 4
        ...
    - Respostas:
        Resposta 1: a|b|c|d. Justificativa.
        Resposta 2: a|b|c|d. Justificativa.
        ...
    Observação: Questões de múltipla escolha para alunos do ensino médio devem possuir 5 alternativas.
    - Exemplo:
    - Questões:
    - 1. Qual é a complexidade de tempo de uma árvore de pesquisa binária balanceada?
        a. O(n)
        b. O(log n)
        c. O(n^2)
        d. O(1)
    - Respostas: 
        1. b.
        Justificativa: A complexidade de tempo de operações em uma árvore de pesquisa binária balanceada é 𝑂(log 𝑛) porque a altura da árvore é proporcional a log 𝑛, permitindo buscas, inserções e remoções em tempo logarítmico.
    - Verdadeiro ou Falso:
    - Questões:
        <Questão1>: <Verdadeiro|Falso>
        <Questão2>: <Verdadeiro|Falso>
            .....
    - Respostas:
        <Resposta1>: <Verdadeiro|Falso>
        <Resposta2>: <Verdadeiro|Falso>
            ...
    - Discursiva:
    - Questões:
        <Questão1>:
        <Questão2>:
        ...
    - Respostas:
        <Resposta1>:
        <Resposta2>:
        ...
    """

    prompt = ChatPromptTemplate.from_template(template)
    prompt.format(quantidade=4, tipo="Múltipla Escolha", disciplina="Ciências", serie="4º Ano do Ensino Fundamental", conteudo="Microrganismos", habilidade="", dificuldade="Médio")

    return prompt

def criar_template_do_prompt_2():
    template = """
    Dado o contexto: {contexto}
    Você é um especialista em inclusão educacional.
    Adapte as questões geradas para alunos com deficiência intelectual.

    Existem as seguintes formas de se adaptar questões:
    1. Separar os objetivos da atividade (Análise de Tarefas)
    2. Adaptar o Layout
    3. Letras em caixa alta (Comando e alternativas com letras maiúsculas)
    4. Adaptar o vocabulário (Simplifique)
    5. Apoio visual (Dê sugestões de imagens adequadas para as questões)
    6. Modelo de exemplo (Mostre um exemplo de como deve ser feita a questão)

    Utilize a(s) forma(s): {forma}
    """
    prompt = ChatPromptTemplate.from_template(template)
    prompt.format(contexto="", forma="[0: '3', 1: '4]")
    return prompt

def criar_chain(prompt_template, llm, chave_api):
    return prompt_template | llm | StrOutputParser()

def main():
    st.title("Gerador de Questões")
    st.write("Crie questões diversas e originais com praticidade.")
    prompt_template_1 = criar_template_do_prompt_1()
    llm = GoogleGenerativeAI(temperature=0.7, model="gemini-1.5-flash")
    chain1 = criar_chain(prompt_template_1, llm, chave_api)
    quantidade = st.number_input("Escolha a quantidade de questões", min_value=1, max_value=10, value=4)
    tipo = st.selectbox("Escolha o tipo de questão", ("Múltipla Escolha", "Verdadeiro ou Falso", "Discursiva"))
    disciplina = st.selectbox("Escolha a disciplina", 
                              ("Português", "Matemática", "Geografia", "História", "Ciências", "Biologia", "Química", "Física",
                               "Sociologia", "Filosofia", "Educação Física", "Inglês", "Espanhol", "Arte"))
    serie = st.selectbox("Escolha a série dos alunos", ("1º Ano do Ensino Fundamental",
                                                        "2º Ano do Ensino Fundamental",
                                                        "3º Ano do Ensino Fundamental",
                                                        "4º Ano do Ensino Fundamental",
                                                        "5º Ano do Ensino Fundamental",
                                                        "6º Ano do Ensino Fundamental",
                                                        "7º Ano do Ensino Fundamental",
                                                        "8º Ano do Ensino Fundamental",
                                                        "9º Ano do Ensino Fundamental",
                                                        "1º Ano do Ensino Médio",
                                                        "2º Ano do Ensino Médio",
                                                        "3º Ano do Ensino Médio"))
    habilidade = st.text_area("Digite a competência/habilidade da BNCC", placeholder="Ex.: (EF01LP15) Agrupar palavras pelo critério de aproximação de significado (sinonímia) e separar palavras pelo critério de oposição de significado (antonímia).")
    conteudo = st.text_area("Digite o conteúdo das questões", placeholder="Ex.: Sinonímia e antonímia")
    dificuldade = st.selectbox("Selecione o nível de dificuldade", ("Fácil", "Médio", "Difícil"))

    if 'resposta1' not in st.session_state:
        st.session_state.resposta1 = None

    if 'botao_template_2' not in st.session_state:
        st.session_state.botao_template_2 = False

    if st.button("Gerar Questões"):
        resposta1 = chain1.invoke({"quantidade":quantidade, "tipo":tipo, "disciplina":disciplina, "serie":serie, "conteudo":conteudo, "habilidade":habilidade, "dificuldade":dificuldade})
        st.session_state.resposta1 = resposta1
        st.write("Questões geradas!")
        st.write(resposta1)
        st.session_state.botao_template_2 = True
    
    prompt_template_2 = criar_template_do_prompt_2()
    chain2 = criar_chain(prompt_template_2, llm, chave_api)
    
    if 'botao_template_2' in st.session_state and st.session_state.botao_template_2:
        st.write("Se deseja adaptar a avaliação, preencha abaixo:")

        st.write("Opções:")
        st.write("1. Separar os objetivos da atividade (Análise de Tarefas)")
        st.write("2. Adaptar o Layout")
        st.write("3. Letras em caixa alta")
        st.write("4. Adaptar o vocabulário")
        st.write("5. Apoio visual")
        st.write("6. Modelo de exemplo")

        forma = st.multiselect("Selecione as adaptações que devem ser feitas",
                               ["1", "2", "3", "4", "5", "6"])
        if st.button("Quero adaptar essa avalição"):
            contexto = st.session_state.resposta1
            resposta2 = chain2.invoke({"contexto":contexto, "forma":forma})
            st.write(resposta2)

main()
    