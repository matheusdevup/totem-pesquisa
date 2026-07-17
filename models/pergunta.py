from database.connection import conectar


def cadastrar_pergunta(
        pesquisa_id,
        texto,
        tipo_resposta,
        obrigatoria):

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO pergunta
        (
            pesquisa_id,
            texto,
            tipo_resposta,
            obrigatoria
        )
        VALUES (?, ?, ?, ?)
    """, (
        pesquisa_id,
        texto,
        tipo_resposta,
        obrigatoria
    ))

    conexao.commit()
    conexao.close()