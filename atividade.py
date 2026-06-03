# MATRIZ 10x4
# Nome | Idade | CPF | Profissão

matriz = [
    ["Carlos", 25, "123.456.789-00", "Engenheiro"],
    ["Maria", 30, "987.654.321-11", "Professora"],
    ["João", 22, "111.222.333-44", "Programador"],
    ["Ana", 28, "555.666.777-88", "Médica"],
    ["Pedro", 35, "999.888.777-66", "Advogado"],
    ["Lucas", 19, "444.333.222-11", "Estudante"],
    ["Fernanda", 40, "777.888.999-00", "Arquiteta"],
    ["Juliana", 27, "222.111.000-99", "Enfermeira"],
    ["Rafael", 33, "666.555.444-33", "Motorista"],
    ["Beatriz", 24, "888.777.666-55", "Designer"]
]

# LOOP PRINCIPAL
while True:

    print("\n===== LISTA DE PESSOAS =====")

    for i, linha in enumerate(matriz):
        print(f"{i} - {linha[0]}")

    alterar = input("\nDeseja alterar algum dado? (sim/não): ").lower()

    if alterar == "não" or alterar == "nao":
        print("\nPrograma encerrado.")
        break

    # Escolher pessoa
    indice = int(input("\nDigite o número da pessoa: "))

    # Escolher campo
    campo = input(
        "Qual dado deseja alterar? (Nome, CPF, idade ou profissão): "
    ).lower()

    # Novo valor
    novo_valor = input("Digite o novo valor: ")

    # ALTERAÇÃO
    if campo == "nome":
        matriz[indice][0] = novo_valor

    elif campo == "idade":
        matriz[indice][1] = int(novo_valor)

    elif campo == "cpf":
        matriz[indice][2] = novo_valor

    elif campo == "profissão":
        matriz[indice][3] = novo_valor

    else:
        print("Campo inválido!")
        continue

    # MOSTRAR LINHA ESPECÍFICA
    print("\n===== DADOS ATUALIZADOS =====")
    print(f"Nome: {matriz[indice][0]}")
    print(f"Idade: {matriz[indice][1]}")
    print(f"CPF: {matriz[indice][2]}")
    print(f"Profissão: {matriz[indice][3]}")

    # VALIDAR DADOS
    confirmar = input("\nOs dados estão corretos? (sim/não): ").lower()

    if confirmar == "não" or confirmar == "nao":

        novo_valor = input("Digite o valor correto: ")

        if campo == "nome":
            matriz[indice][0] = novo_valor

        elif campo == "idade":
            matriz[indice][1] = int(novo_valor)

        elif campo == "cpf":
            matriz[indice][2] = novo_valor

        elif campo == "profissão":
            matriz[indice][3] = novo_valor

        print("\nDados corrigidos com sucesso!")

    print("\nAlteração finalizada.")