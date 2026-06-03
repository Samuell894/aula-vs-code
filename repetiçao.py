resposta = "s"

while resposta == "s":
    num1 = float(input("Digite o primeiro número: "))
    num2 = float(input("Digite o segundo número: "))
    
    soma = num1 + num2
    print("Resultado da soma:", soma)
    
    resposta = input("Deseja fazer outra soma? (s/n): ").lower()

print("Programa encerrado.")