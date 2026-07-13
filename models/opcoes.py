import sqlite3
from database.connection import conectar

def cadastrar_opcoes(pergunta_id,texto):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(
        "INSERT INTO opcoes (pergunta_id, texto) VALUES (?, ?)",
        (pergunta_id,texto)
    )
    conexao.commit()
    print("Opção Criada com Sucesso!")
    conexao.close()

def consultar_opcoes(pergunta_id):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM opcoes WHERE pergunta_id = ?", (pergunta_id,))
    opcoes = cursor.fetchall()
    conexao.close()
    return opcoes

def atualizar_opcoes(id,pergunta_id,texto):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(
        """
        UPDATE opcoes
        SET
            pergunta_id = ?,
            texto = ?
        WHERE id = ?
        """,
        (
            pergunta_id,
            texto,
            id
        )
    )
    conexao.commit()
    print("Opção atualizada com sucesso!")
    conexao.close()

def excluir_opcoes(id):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM opcoes WHERE id = ?",(id,))
    conexao.commit()
    print ("Opção foi deletada com sucesso!")
    conexao.close()