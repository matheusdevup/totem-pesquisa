import sqlite3
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