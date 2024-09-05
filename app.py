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

def criar_template_do_prompt():

    template = """
    Você é um professor especialista em criar questões em todos os campos de conhecimento.
    Pense passo a passo e elabore uma avaliação com {quantidade} questões do tipo {tipo}, da disciplina {disciplina},
    para alunos do {serie}, sobre o conteúdo {conteudo} e com nível de dificuldade {dificuldade}.

    O formato das questões é um dos seguintes:
    - Múltipla Escolha:
    - Questões:
        <Questão1>: 
            <a. Resposta 1></n>
            <b. Resposta 2></n>
            <c. Resposta 3></n>
            <d. Resposta 4></n>
        <Questão2>: 
            <a. Resposta 1></n>
            <b. Resposta 2></n>
            <c. Resposta 3></n>
            <d. Resposta 4></n>
        ...
    - Respostas:
        <Resposta1>: <a|b|c|d>.</n> Justificativa.
        <Resposta2>: <a|b|c|d>.</n> Justificativa.
        ...
    Observação: Questões de múltipla escolha para alunos do ensino médio devem possuir 5 alternativas.
    - Exemplo:
    - Questões:
    - 1. Qual é a complexidade de tempo de uma árvore de pesquisa binária balanceada?
        a. O(n)</n>
        b. O(log n)</n>
        c. O(n^2)</n>
        d. O(1)</n>
    - Respostas: 
        1. b.</n>
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
    prompt.format(quantidade=4, tipo="Múltipla Escolha", disciplina="Ciências", serie="4º Ano do Ensino Fundamental", conteudo="Microrganismos", dificuldade="Médio")

    return prompt

def criar_chain(prompt_template, llm, chave_api):
    return prompt_template | llm | StrOutputParser()

def main():
    st.title("Gerador de Questões")
    st.write("Crie questões diversas e originais com praticidade.")
    prompt_template = criar_template_do_prompt()
    llm = GoogleGenerativeAI(temperature=0.7, model="gemini-1.5-flash")
    chain = criar_chain(prompt_template, llm, chave_api)
    quantidade = st.number_input("Escolha a quantidade de questões", min_value=1, max_value=10, value=4)
    tipo = st.selectbox("Escolha o tipo de questão", ("Múltipla Escolha", "Verdadeiro ou Falso", "Discursiva"))
    disciplina = st.selectbox("Escolha a disciplina", 
                              ("Português", "Matemática", "Geografia", "História", "Ciências", "Biologia", "Química", "Física",
                               "Sociologia", "Filosofia", "Educação Física"))
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
    conteudo = st.text_area("Digite o conteúdo das questões")
    dificuldade = st.selectbox("Selecione o nível de dificuldade", ("Fácil", "Médio", "Difícil"))

    if st.button("Gerar Questões"):
        resposta = chain.invoke({"quantidade":quantidade, "tipo":tipo, "disciplina":disciplina, "serie":serie, "conteudo":conteudo, "dificuldade":dificuldade})
        st.write("Questões geradas!")
        st.write(resposta)

if __name__ == "__main__":
    main()
    