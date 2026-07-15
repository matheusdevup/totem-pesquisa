from database.connection import conectar


def criar_tabelas():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS funcionarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cpf TEXT NOT NULL,
            nome TEXT NOT NULL,
            setor TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pesquisa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT,
            descricao TEXT NOT NULL,
            imagem TEXT NOT NULL,
            data_inicio TEXT,
            data_fim TEXT,
            status TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS perguntas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pesquisa_id INTEGER NOT NULL,
            pergunta TEXT NOT NULL,
            tipo TEXT NOT NULL,
            obrigatoria INTEGER NOT NULL DEFAULT 1,
            ordem INTEGER,
            valor_min INTEGER,
            valor_max INTEGER,
            FOREIGN KEY (pesquisa_id) REFERENCES pesquisa(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS respostas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            funcionario_id INTEGER NOT NULL,
            pergunta_id INTEGER NOT NULL,
            resposta TEXT NOT NULL,
            data_resposta DATETIME NOT NULL,
            FOREIGN KEY (funcionario_id) REFERENCES funcionarios(id),
            FOREIGN KEY (pergunta_id) REFERENCES perguntas(id)
        )
    """)

    conexao.commit()
    cursor.close()
    conexao.close()

    print("Tabelas criadas com sucesso.")


if __name__ == "__main__":
    criar_tabelas() 