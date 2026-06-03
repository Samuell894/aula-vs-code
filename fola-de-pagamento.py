print("=================== Folha de pagamento ===================")
# Entrada de dados
valor_hora = float(input("Digite o valor da sua hora: R$ "))
horas_trabalhadas = float(input("Digite a quantidade de horas trabalhadas no mês: "))
# Cálculo do salário bruto
salario_bruto = valor_hora * horas_trabalhadas
# Cálculo do IR
if salario_bruto <= 900:
    percentual_ir = 0
elif salario_bruto <= 1500:
    percentual_ir = 5
elif salario_bruto <= 2500:
    percentual_ir = 10
else:
    percentual_ir = 20
valor_ir = salario_bruto * (percentual_ir / 100)
# Cálculo do INSS (10%)
valor_inss = salario_bruto * 0.10
# Cálculo do FGTS (11%) – não desconta
valor_fgts = salario_bruto * 0.11
# Total de descontos
total_descontos = valor_ir + valor_inss
# Salário líquido
salario_liquido = salario_bruto - total_descontos
# Saída de dados
print(f"\nSalário bruto ({valor_hora} * {horas_trabalhadas}): R$ {salario_bruto:.2f}")
print(f"(-) IR ({percentual_ir}%): R$ {valor_ir:.2f}")
print(f"(-) INSS (10%): R$ {valor_inss:.2f}")
print(f"FGTS (11%): R$ {valor_fgts:.2f}")
print(f"Total de descontos: R$ {total_descontos:.2f}")
print(f"Salário líquido: R$ {salario_liquido:.2f}")