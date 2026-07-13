from models.funcionarios import consultar_funcionario
from models.pesquisa import consultar_pesquisas
from models.perguntas import consultar_perguntas
from models.resposta import (
    cadastrar_respostas,
    funcionario_ja_respondeu_pesquisa
)
from services.validacao_resposta import (
    validar_resposta_escala,
    validar_resposta_numero,
    validar_resposta_sim_nao,
    validar_resposta_texto
)


while True:
    print("\n=== TOTEM DE PESQUISAS ===")

    entrada_cpf = input("Digite seu CPF: ").strip()

    if not entrada_cpf.isdigit():
        print("\nCPF inválido. Digite somente números.")
        continue

    cpf = int(entrada_cpf)
    funcionario = consultar_funcionario(cpf)

    if funcionario is None:
        print("\nFuncionário não encontrado.")
        continue

    print(f"\nBem-vindo, {funcionario[2]}!")

    while True:
        print("\n=== PESQUISAS DISPONÍVEIS ===")

        pesquisas = consultar_pesquisas()

        if not pesquisas:
            print("\nNão existem pesquisas disponíveis.")
            break

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
            break

        perguntas = consultar_perguntas(pesquisa_id)

        if not perguntas:
            print(
                "\nPesquisa inválida ou "
                "sem perguntas cadastradas."
            )
            continue

        if funcionario_ja_respondeu_pesquisa(
            funcionario[0],
            pesquisa_id
        ):
            print("\nVocê já respondeu esta pesquisa.")
            continue

        print("\n=== INÍCIO DA PESQUISA ===")

        for pergunta in perguntas:
            tipo = pergunta[3].strip().lower()
            obrigatoria = pergunta[4] == 1

            print(f"\n{pergunta[2]}")

            if obrigatoria:
                print("* Pergunta obrigatória")
            else:
                print(
                    "Pergunta opcional. "
                    "Pressione Enter para pular."
                )

            if tipo == "escala":
                resposta = validar_resposta_escala(
                    pergunta[6],
                    pergunta[7],
                    obrigatoria
                )

            elif tipo == "numero":
                resposta = validar_resposta_numero(
                    obrigatoria
                )

            elif tipo == "sim_nao":
                resposta = validar_resposta_sim_nao(
                    obrigatoria
                )

            elif tipo == "texto":
                resposta = validar_resposta_texto(
                    obrigatoria
                )

            else:
                print(
                    f"Tipo de pergunta não reconhecido: {tipo}"
                )
                continue

            if resposta is None:
                print("Pergunta ignorada.")
                continue

            cadastrar_respostas(
                funcionario[0],
                pergunta[0],
                resposta
            )

        print("\nPesquisa respondida com sucesso!")