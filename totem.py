from services.fluxo_totem import (
    autenticar_funcionario,
    selecionar_pesquisa,
    responder_pesquisa
)

while True:
    print("\n=== TOTEM DE PESQUISAS ===")

    funcionario = autenticar_funcionario()

    if funcionario is None:
        continue

    while True:
        pesquisa_id = selecionar_pesquisa()

        if pesquisa_id is None:
            break

        responder_pesquisa(
            funcionario,
            pesquisa_id
        )