from banco import criar_tabela, listar_produtos

criar_tabela()

produtos = listar_produtos()

for produto in produtos:
    print(f"ID: {produto[0]}")
    print(f"Nome: {produto[1]}")
    print(f"Quantidade: {produto[2]}")
    print(f"Mínimo: {produto[3]}")
    print("-" * 30)