arquivo = open("configurador_gigante.py", "w", encoding="utf-8")

# Cabeçalho
arquivo.write("from datetime import datetime\n\n")
arquivo.write("print('========== CONFIGURADOR DE CARROS ==========' )\n\n")
arquivo.write("agora = datetime.now()\n")
arquivo.write("data = agora.strftime('%d/%m/%Y')\n")
arquivo.write("hora = agora.strftime('%H:%M:%S')\n\n")

# Marca
arquivo.write("print('\\nEscolha a Marca:')\n")
arquivo.write("print('1 - BMW')\n")
arquivo.write("print('2 - Audi')\n")
arquivo.write("marca = input('Digite a opção: ')\n\n")

indent = ""

# MARCA
for m in range(1, 3):
    if m == 1:
        marca_nome = "BMW"
    else:
        marca_nome = "Audi"

    arquivo.write(indent + f"if marca == '{m}':\n")
    indent += "    "
    arquivo.write(indent + f"marca_nome = '{marca_nome}'\n\n")

    # MODELOS
    arquivo.write(indent + "print('\\nEscolha o Modelo:')\n")

    if marca_nome == "BMW":
        modelos = [
            ("Série 1", "140cv", "Gasolina"),
            ("Série 3", "184cv", "Gasolina"),
            ("Série 5", "252cv", "Gasolina"),
            ("X1", "150cv", "Diesel"),
            ("X3", "190cv", "Diesel"),
            ("X5", "265cv", "Diesel"),
        ]
    else:
        modelos = [
            ("A1", "110cv", "Gasolina"),
            ("A3", "150cv", "Gasolina"),
            ("A4", "204cv", "Diesel"),
            ("A6", "265cv", "Diesel"),
            ("Q3", "150cv", "Gasolina"),
            ("Q5", "204cv", "Diesel"),
        ]

    for i, modelo in enumerate(modelos, start=1):
        arquivo.write(indent + f"print('{i} - {modelo[0]} ({modelo[1]} {modelo[2]})')\n")

    arquivo.write(indent + "modelo = input('Digite a opção: ')\n\n")

    for i, modelo in enumerate(modelos, start=1):
        arquivo.write(indent + f"if modelo == '{i}':\n")
        arquivo.write(indent + f"    modelo_nome = '{marca_nome} {modelo[0]}'\n")
        arquivo.write(indent + f"    potencia = '{modelo[1]}'\n")
        arquivo.write(indent + f"    combustivel = '{modelo[2]}'\n")
        arquivo.write(indent + "else:\n")
        arquivo.write(indent + "    pass\n")

    indent = indent[:-4]
    arquivo.write("else:\n")
    arquivo.write("    pass\n\n")

# ANO
arquivo.write("print('\\nEscolha o Ano:')\n")
for i in range(2018, 2024):
    arquivo.write(f"print('{i-2017} - {i}')\n")

arquivo.write("ano_op = input('Digite a opção: ')\n")

for i in range(1, 7):
    arquivo.write(f"if ano_op == '{i}':\n")
    arquivo.write(f"    ano = '{2017+i}'\n")
    arquivo.write("else:\n")
    arquivo.write("    pass\n")

# RESULTADO FINAL
arquivo.write("""
print("\\n=========== RESULTADO FINAL ===========")
print("Data:", data)
print("Hora:", hora)
print("---------------------------------------")
print("Marca:", marca_nome)
print("Modelo:", modelo_nome)
print("Ano:", ano)
print("\\n--- CARACTERÍSTICAS TÉCNICAS ---")
print("Potência:", potencia)
print("Combustível:", combustivel)
print("=======================================")
""")

arquivo.close()

print("Ficheiro configurador_gigante.py criado com sucesso!")
