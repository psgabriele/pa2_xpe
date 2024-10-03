from db.conexao import conectar_ao_db

def salva_avaliacao(usuario_id, quantidade, tipo, disciplina, serie, habilidade, conteudo, nivel):
    conexao = conectar_ao_db()
    cursor = conexao.cursor()

    # Insere os dados da avaliação no banco de dados
    query = 'INSERT INTO avaliacao (usuario_id, qnt_questao, tipo, disciplina, serie, habilidade, conteudo, nivel) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
    values = (usuario_id, quantidade, tipo, disciplina, serie, habilidade, conteudo, nivel)
    cursor.execute(query, values)
    
    conexao.commit()

    cursor.close()
    conexao.close()
    # Retorna o ID da avaliação recém-inserida
    return cursor.lastrowid

# Função para buscar as avaliações do usuário a partir do banco de dados
def buscar_avaliacoes(usuario_id, disciplina=None, serie=None, nivel=None, texto_busca=None):
    conexao = conectar_ao_db()
    cursor = conexao.cursor()

    # Consulta SQL básica
    query = """
    SELECT id, qnt_questao, tipo, disciplina, serie, habilidade, conteudo, nivel, created_at
    FROM avaliacao 
    WHERE usuario_id = %s
    """
    params = [usuario_id]

    # Adicionar filtros dinamicamente se forem fornecidos
    if disciplina:
        query += " AND disciplina = %s"
        params.append(disciplina)
    if serie:
        query += " AND serie = %s"
        params.append(serie)
    if nivel:
        query += " AND nivel = %s"
        params.append(nivel)

    # Busca por texto no conteúdo ou habilidade
    if texto_busca:
        query += " AND (conteudo LIKE %s OR habilidade LIKE %s)"
        params.append(f"%{texto_busca.strip()}%")
        params.append(f"%{texto_busca.strip()}%")  # Usar LIKE para busca parcial

    # Depuração: Ver query e parâmetros
    print(f"Query: {query}")
    print(f"Parâmetros: {params}")

    cursor.execute(query, tuple(params))  # Executar a query com os parâmetros
    avaliacoes = cursor.fetchall()

    cursor.close()
    conexao.close()

    return avaliacoes

def buscar_opcoes_filtro(campo):
    conexao = conectar_ao_db()
    cursor = conexao.cursor()

    # Consulta SQL para obter valores únicos do campo desejado (disciplina, série, etc.)
    query = f"SELECT DISTINCT {campo} FROM avaliacao"

    cursor.execute(query)
    opcoes = [item[0] for item in cursor.fetchall()]

    cursor.close()
    conexao.close()

    return opcoes

def excluir_avaliacao(avaliacao_id):
    conexao = conectar_ao_db()
    cursor = conexao.cursor()
    query = "DELETE FROM avaliacao WHERE id = %s"
    cursor.execute(query, (avaliacao_id,))
    conexao.commit()
    cursor.close()
    conexao.close()
