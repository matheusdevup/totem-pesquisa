from models.funcionarios import consultar_funcionario
from models.pesquisa import consultar_pesquisas
from models.perguntas import consultar_perguntas
from models.resposta import cadastrar_respostas

while True:
    print("=== TOTEM DE PESQUISAS ===")
    cpf = int(input("Digite seu CPF: "))
    funcionario = consultar_funcionario(cpf)

    if funcionario is None :
        print("Cpf Invalido")

    elif funcionario :
        print(f'\nBem-Vindo {funcionario[2]}')

        for pesquisa in consultar_pesquisas():
            print (f'\n[{pesquisa[0]}] {pesquisa[1]}')

        lista_de_pesquisa = int(input("\nDigite o Id da pesquisa: "))

        lista_de_perguntas = consultar_perguntas(lista_de_pesquisa)

        print (lista_de_perguntas)
        for pergunta in lista_de_perguntas :
            print (f'\n{pergunta[2]}')
            resposta = (input("R: "))
            cadastrar_respostas(funcionario[0], pergunta[0] , resposta)
            print("Resposta salva")

