from db.conexao import conectar_ao_db
import re

def inserir_questoes_respostas(avaliacao_id, questoes, respostas):
    conexao = conectar_ao_db()
    cursor = conexao.cursor()

    """
    Insere perguntas e respostas na tabela questoes_respostas para uma avaliação específica.
    """
    query = '''
        INSERT INTO questoes_respostas (avaliacao_id, questao, resposta) 
        VALUES (%s, %s, %s)
    '''
    
    for questao, resposta in zip(questoes, respostas):
        valores = (avaliacao_id, questao, resposta)
        cursor.execute(query, valores)

    conexao.commit()

    cursor.close()
    conexao.close()

    # Função para buscar questões e respostas de uma avaliação específica
def buscar_questoes_respostas(avaliacao_id):
    conexao = conectar_ao_db()
    cursor = conexao.cursor()

    # Consulta SQL para pegar as questões e respostas
    query = "SELECT questao, resposta FROM questoes_respostas WHERE avaliacao_id = %s"
    cursor.execute(query, (avaliacao_id,))

    # Recupera todos os resultados
    questoes_respostas = cursor.fetchall()

    cursor.close()
    conexao.close()

    return questoes_respostas

def lista_questoes_respostas(avaliacao_id):
    conexao = conectar_ao_db()
    cursor = conexao.cursor()
    query = "SELECT questao, resposta FROM questoes_respostas WHERE id = %s"
    cursor.execute(query, (avaliacao_id,))
    result = cursor.fetchone()

    cursor.close()
    conexao.close()

    if result:
        questoes_texto = result[0]  # Texto das questões concatenadas
        respostas_texto = result[1]  # Texto das respostas concatenadas

        # Separar as questões e respostas usando regex (ou outro método)
        padrao_questoes = r"Questão\s\d+:(.*?)\n"  # Supondo esse padrão no texto
        padrao_respostas = r"Resposta\s\d+: (.*?)\n"  # Supondo esse padrão no texto

        lista_questoes = re.findall(padrao_questoes, questoes_texto, re.DOTALL)
        lista_respostas = re.findall(padrao_respostas, respostas_texto, re.DOTALL)

        return lista_questoes, lista_respostas
    else:
        return [], []

def editar_questoes_respostas(questao_editada, resposta_editada):
    conexao = conectar_ao_db()
    cursor = conexao.cursor()

    # Query de atualização de questão e resposta
    query = """
    UPDATE questoes_respostas 
    SET questao = %s, resposta = %s 
    WHERE id = %s
    """
    cursor.execute(query, (questao_editada, resposta_editada))

    conexao.commit()
    cursor.close()
    conexao.close()

