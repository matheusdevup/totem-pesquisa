import sqlite3
from database.connection import conectar


def cadastrar_pesquisa(titulo, descricao, imagem, data_inicio, data_fim):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(
        "INSERT INTO pesquisa (status, titulo, descricao, imagem, data_inicio, data_fim) VALUES (?, ?, ?, ?, ?, ?)",
        ("Rascunho", titulo, descricao, imagem, data_inicio, data_fim)
    )
    conexao.commit()
    print("Pesquisa Criada com Sucesso!")
    conexao.close()


def consultar_pesquisas():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM pesquisa")
    pesquisas = cursor.fetchall()
    conexao.close()
    return pesquisas


def consultar_pesquisa(id):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM pesquisa WHERE id = ?", (id,))
    pesquisa = cursor.fetchone()
    conexao.close()
    return pesquisa


def atualizar_pesquisa(id, titulo, descricao, imagem, data_inicio, data_fim, status):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(
        """
        UPDATE pesquisa
        SET
            titulo = ?,
            descricao = ?,
            imagem = ?,
            data_inicio = ?,
            data_fim = ?,
            status = ?
        WHERE id = ?
        """,
        (
            titulo,
            descricao,
            imagem,
            data_inicio,
            data_fim,
            status,
            id
        )
    )
    conexao.commit()
    print("Pesquisa atualizada com sucesso!")
    conexao.close()


def excluir_pesquisa(id):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM pesquisa WHERE id = ?", (id,))
    conexao.commit()
    print("Pesquisa foi deletada com sucesso!")
    conexao.close()


def ultima_pesquisa():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT MAX(id)
        FROM pesquisa
    """)

    id = cursor.fetchone()[0]
    conexao.close()
    return id


def consultar_pesquisas_respondidas_usuario(cpf):
    conexao = conectar()
    cursor = conexao.cursor()
    try:
        cursor.execute("SELECT DISTINCT pesquisa_id FROM respostas WHERE funcionario_cpf = ?", (cpf,))
        linhas = cursor.fetchall()
        respondidas_ids = [linha[0] for linha in linhas]
    except sqlite3.OperationalError:
        respondidas_ids = []

    conexao.close()
    return respondidas_ids


def registrar_resposta_usuario(pesquisa_id, cpf):
    conexao = conectar()
    cursor = conexao.cursor()

    # Garante que a tabela de respostas exista
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS respostas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pesquisa_id INTEGER,
            funcionario_cpf TEXT
        )
    """)

    # Insere a confirmação de resposta do usuário
    cursor.execute(
        "INSERT INTO respostas (pesquisa_id, funcionario_cpf) VALUES (?, ?)",
        (pesquisa_id, cpf)
    )
    conexao.commit()
    conexao.close()


if __name__ == "__main__":
    cadastrar_pesquisa(
        "Clima Organizacional 2026",
        "Queremos ouvir você sobre o nosso ambiente de trabalho.",
        "link_da_imagem.png",
        "2026-07-01",
        "2026-07-31"
    )