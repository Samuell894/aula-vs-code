# Saldo inicial
saldo = 0.0

while True:
    print("\n=== Menu Bancário ===")
    print("(a) Consultar saldo")
    print("(b) Saque")
    print("(c) Depósito")
    print("(d) Sair")

    opcao = input("Escolha uma opção: ")

    if opcao == "a":
        print(f"Seu saldo atual é: R$ {saldo:.2f}")
    elif opcao == "b":
        valor = float(input("Digite o valor do saque: "))
        if valor <= saldo:
            saldo -= valor
            print(f"Saque realizado! Novo saldo: R$ {saldo:.2f}")
        else:
            print("Saldo insuficiente!")
    elif opcao == "c":
        valor = float(input("Digite o valor do depósito: "))
        saldo += valor
        print(f"Depósito realizado! Novo saldo: R$ {saldo:.2f}")
    elif opcao == "d":
        print("Encerrando o programa...")
        break
    else:
        print("Opção inválida! Tente novamente.")