from database.connection import conectar
from datetime import datetime


def cadastrar_respostas(funcionario_id, pergunta_id, resposta):
    data = datetime.now()
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(
        "INSERT INTO respostas (funcionario_id, pergunta_id, resposta, data_resposta) VALUES (?, ?, ?, ?)",
        (funcionario_id, pergunta_id, resposta, data)
    )
    conexao.commit()
    print("Resposta criada com sucesso!")
    conexao.close()

def consultar_respostas_por_funcionario(funcionario_id):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM respostas WHERE funcionario_id = ?", (funcionario_id,))
    respostas = cursor.fetchall()
    conexao.close()
    return respostas


def consultar_respostas_por_pesquisa(conexao, pesquisa_id):
    cursor = conexao.cursor()
    comando_sql = """
        SELECT respostas.* FROM respostas
        INNER JOIN perguntas ON respostas.pergunta_id = perguntas.id
        WHERE perguntas.pesquisa_id = ?
    """
    cursor.execute(comando_sql, (pesquisa_id,))
    respostas = cursor.fetchall()
    cursor.close()

    return respostas

def funcionario_ja_respondeu_pesquisa(funcionario_id, pesquisa_id):
    conexao = conectar()
    cursor = conexao.cursor()

    comando_sql = """
        SELECT 1
        FROM respostas AS r
        INNER JOIN perguntas AS p
            ON r.pergunta_id = p.id
        WHERE r.funcionario_id = ?
          AND p.pesquisa_id = ?
        LIMIT 1
    """

    cursor.execute(comando_sql, (funcionario_id, pesquisa_id))
    resultado = cursor.fetchone()

    cursor.close()
    conexao.close()

    return resultado is not None
