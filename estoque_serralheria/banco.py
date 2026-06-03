import sqlite3

def conectar():
    return sqlite3.connect("estoque.db")


def criar_tabela():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        quantidade INTEGER NOT NULL,
        minimo INTEGER NOT NULL
    )
    """)

    conexao.commit()
    conexao.close()


def adicionar_produto(nome, quantidade, minimo):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
    INSERT INTO produtos (nome, quantidade, minimo)
    VALUES (?, ?, ?)
    """, (nome, quantidade, minimo))

    conexao.commit()
    conexao.close()

    print(f"Produto '{nome}' cadastrado com sucesso!")



def listar_produtos():

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM produtos")

    produtos = cursor.fetchall()

    conexao.close()

    return produtos