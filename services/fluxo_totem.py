from models.funcionarios import consultar_funcionario
from models.pesquisa import consultar_pesquisas
from models.perguntas import consultar_perguntas
from models.resposta import (
    cadastrar_respostas,
    funcionario_ja_respondeu_pesquisa
)
from services.resposta_pergunta import obter_resposta


def autenticar_funcionario():
    entrada_cpf = input("Digite seu CPF: ").strip()

    if not entrada_cpf.isdigit():
        print("\nCPF inválido. Digite somente números.")
        return None

    cpf = int(entrada_cpf)
    funcionario = consultar_funcionario(cpf)

    if funcionario is None:
        print("\nFuncionário não encontrado.")
        return None

    print(f"\nBem-vindo, {funcionario[2]}!")
    return funcionario

def selecionar_pesquisa():

    while True:

        print("\n=== PESQUISAS DISPONÍVEIS ===")

        pesquisas = consultar_pesquisas()

        if not pesquisas:
            print("\nNão existem pesquisas disponíveis.")
            return None

        for pesquisa in pesquisas:
            print(f"[{pesquisa[0]}] {pesquisa[1]}")

        print("[0] Encerrar atendimento")

        entrada_pesquisa = input(
            "\nDigite o ID da pesquisa: "
        ).strip()

        if not entrada_pesquisa.isdigit():
            print(
                "\nOpção inválida. "
                "Digite somente o número da pesquisa."
            )
            continue

        pesquisa_id = int(entrada_pesquisa)

        if pesquisa_id == 0:
            print("\nAtendimento encerrado.")
            return None

        for pesquisa in pesquisas:
            if pesquisa[0] == pesquisa_id:
                return pesquisa_id

        print("\nPesquisa inválida.")

def responder_pesquisa(funcionario, pesquisa_id):

    perguntas = consultar_perguntas(pesquisa_id)

    if not perguntas:
        print("\nPesquisa inválida ou sem perguntas cadastradas.")
        return

    if funcionario_ja_respondeu_pesquisa(
        funcionario[0],
        pesquisa_id
    ):
        print("\nVocê já respondeu esta pesquisa.")
        return

    for pergunta in perguntas:

        print(f"\n{pergunta[2]}")

        if pergunta[4]:
            print("* Pergunta obrigatória")
        else:
            print("Pergunta opcional. Pressione Enter para pular.")

        resposta = obter_resposta(pergunta)

        if resposta is None:
            print("Pergunta ignorada.")
            continue

        cadastrar_respostas(
            funcionario[0],
            pergunta[0],
            resposta
        )

    print("\nPesquisa respondida com sucesso!")




if __name__ == "__main__":
    pesquisas = consultar_pesquisas()
    print(pesquisas)