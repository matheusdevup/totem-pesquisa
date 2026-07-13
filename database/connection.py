import sqlite3
from pathlib import Path

PASTA_ATUAL = Path(__file__).parent
CAMINHO_BANCO = PASTA_ATUAL / "totem.db"

def conectar() :
    conexao = sqlite3.connect(CAMINHO_BANCO)
    return conexao

if __name__ == "__main__":
    resultado = conectar()
    print(resultado)