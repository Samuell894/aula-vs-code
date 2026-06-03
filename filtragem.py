from datetime import datetime

print("=== CONFIGURADOR DE CARROS ===")

agora = datetime.now()
data = agora.strftime("%d/%m/%Y")
hora = agora.strftime("%H:%M:%S")

# =========================
# 1 - MARCA
# =========================

print("\nEscolha a Marca:")
print("1 - BMW")
print("2 - Audi")

marca = input("Digite a opção: ")

if marca == "1":
    marca_nome = "BMW"
else:
    if marca == "2":
        marca_nome = "Audi"
    else:
        print("Marca inválida!")
        exit()

# =========================
# 2 - MODELOS REAIS
# =========================

if marca_nome == "BMW":

    print("\nModelos BMW:")
    print("1 - Série 1")
    print("2 - Série 3")
    print("3 - Série 5")
    print("4 - X1")
    print("5 - X3")
    print("6 - X5")

    modelo = input("Escolha o modelo: ")

    if modelo == "1":
        modelo_nome = "Série 1"
    else:
        if modelo == "2":
            modelo_nome = "Série 3"
        else:
            if modelo == "3":
                modelo_nome = "Série 5"
            else:
                if modelo == "4":
                    modelo_nome = "X1"
                else:
                    if modelo == "5":
                        modelo_nome = "X3"
                    else:
                        if modelo == "6":
                            modelo_nome = "X5"
                        else:
                            print("Modelo inválido!")
                            exit()

else:

    print("\nModelos Audi:")
    print("1 - A1")
    print("2 - A3")
    print("3 - A4")
    print("4 - A6")
    print("5 - Q3")
    print("6 - Q5")

    modelo = input("Escolha o modelo: ")

    if modelo == "1":
        modelo_nome = "A1"
    else:
        if modelo == "2":
            modelo_nome = "A3"
        else:
            if modelo == "3":
                modelo_nome = "A4"
            else:
                if modelo == "4":
                    modelo_nome = "A6"
                else:
                    if modelo == "5":
                        modelo_nome = "Q3"
                    else:
                        if modelo == "6":
                            modelo_nome = "Q5"
                        else:
                            print("Modelo inválido!")
                            exit()


# =========================
# 3 - ANO
