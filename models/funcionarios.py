import sqlite3
from database.connection import conectar


def cadastrar_funcionario(cpf, nome, setor):
    conexao = conectar()
    cursor = conexao.cursor()
    try:
        cursor.execute(
            "INSERT INTO funcionarios (cpf, nome, setor) VALUES (?, ?, ?)",
            (cpf, nome, setor)
        )
        conexao.commit()
        print("Funcionário cadastrado com sucesso!")
    except sqlite3.IntegrityError:
        print("Erro: este CPF já está cadastrado.")
    conexao.close()


def consultar_funcionario(cpf):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM funcionarios WHERE cpf = ?", (cpf,))
    funcionario = cursor.fetchone()
    conexao.close()
    return funcionario


if __name__ == "__main__":
    cadastrar_funcionario("11398410926", "Matheus", "Suporte TI")
    resultado = consultar_funcionario("11398410926")
    if resultado:
        print("\nSucesso! Usuário encontrado:")
        print(resultado)
    else:
        print("CPF não encontrado.")