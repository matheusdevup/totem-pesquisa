from services.validacao_resposta import (
    validar_resposta_escala,
    validar_resposta_numero,
    validar_resposta_sim_nao,
    validar_resposta_texto
)

def obter_resposta(pergunta):

    tipo = pergunta[3].strip().lower()
    obrigatoria = pergunta[4] == 1

    if tipo == "escala":
        return validar_resposta_escala(
            pergunta[6],
            pergunta[7],
            obrigatoria
        )

    elif tipo == "numero":
        return validar_resposta_numero(
            obrigatoria
        )

    elif tipo == "sim_nao":
        return validar_resposta_sim_nao(
            obrigatoria
        )

    elif tipo == "texto":
        return validar_resposta_texto(
            obrigatoria
        )

    print(f"Tipo de pergunta inválido: {tipo}")
    return None