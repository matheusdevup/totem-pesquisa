def validar_resposta_escala(valor_min, valor_max, obrigatoria):
    while True:
        print(f"Digite um valor entre {valor_min} e {valor_max}.")

        resposta = input("R: ").strip()

        if not resposta and not obrigatoria:
            return None

        if not resposta and obrigatoria:
            print(
                "Esta pergunta é obrigatória. "
                "Digite uma resposta."
            )
            continue

        if resposta.isdigit():
            resposta_numerica = int(resposta)

            if valor_min <= resposta_numerica <= valor_max:
                return resposta

        print(
            f"Resposta inválida. Digite um número "
            f"entre {valor_min} e {valor_max}."
        )


def validar_resposta_numero(obrigatoria):
    while True:
        print("Digite somente um número.")

        resposta = input("R: ").strip()

        if not resposta and not obrigatoria:
            return None

        if not resposta and obrigatoria:
            print(
                "Esta pergunta é obrigatória. "
                "Digite uma resposta."
            )
            continue

        if resposta.isdigit():
            return resposta

        print(
            "Resposta inválida. "
            "Digite somente um número."
        )


def validar_resposta_sim_nao(obrigatoria):
    while True:
        print("Digite 'sim' ou 'não'.")

        resposta = input("R: ").strip().lower()

        if not resposta and not obrigatoria:
            return None

        if not resposta and obrigatoria:
            print(
                "Esta pergunta é obrigatória. "
                "Digite uma resposta."
            )
            continue

        if resposta in ("sim", "não", "nao"):
            if resposta == "nao":
                resposta = "não"

            return resposta

        print(
            "Resposta inválida. "
            "Digite 'sim' ou 'não'."
        )


def validar_resposta_texto(obrigatoria):
    while True:
        print("Digite sua resposta em texto.")

        resposta = input("R: ").strip()

        if resposta:
            return resposta

        if not obrigatoria:
            return None

        print(
            "Esta pergunta é obrigatória. "
            "Digite uma resposta."
        )