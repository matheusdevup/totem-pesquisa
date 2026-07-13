import sqlite3
from database.connection import conectar

def cadastrar_perguntas(pesquisa_id, pergunta, tipo, obrigatoria, ordem, valor_min, valor_max):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(
        "INSERT INTO perguntas (pesquisa_id, pergunta, tipo, obrigatoria, ordem, valor_min, valor_max) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (pesquisa_id, pergunta, tipo, obrigatoria, ordem, valor_min, valor_max)
    )
    conexao.commit()
    print("Pergunta criada com sucesso!")
    conexao.close()

def consultar_perguntas(pesquisa_id):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM perguntas WHERE pesquisa_id = ?", (pesquisa_id,))
    perguntas = cursor.fetchall()
    conexao.close()
    return perguntas

def atualizar_perguntas(id,pesquisa_id, pergunta, tipo, obrigatoria, ordem, valor_min, valor_max):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(
        """
        UPDATE perguntas
        SET
            pesquisa_id = ?,
            pergunta = ?,
            tipo = ?,
            obrigatoria = ?,
            ordem = ?,
            valor_min = ?,
            valor_max = ?
        WHERE id = ?
        """,
        (
            pesquisa_id,
            pergunta,
            tipo,
            obrigatoria,
            ordem,
            valor_min,
            valor_max,
            id
        )
    )
    conexao.commit()
    print("Pergunta atualizada com sucesso!")
    conexao.close()

def excluir_perguntas(id):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM perguntas WHERE id = ?",(id,))
    conexao.commit()
    print ("Pergunta foi deletada com sucesso!")
    conexao.close()


if __name__ == "__main__":
    # Vamos cadastrar duas perguntas para a pesquisa ID 1
    # Parâmetros: pesquisa_id, pergunta, tipo, obrigatoria, ordem, valor_min, valor_max

    cadastrar_perguntas(1, "Como você avalia seu ambiente de trabalho?", "escala", 1, 1, 1, 5)
    cadastrar_perguntas(1, "Deixe um feedback ou sugestão de melhoria:", "texto", 0, 2, None, None)