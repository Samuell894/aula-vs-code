import sqlite3
import customtkinter as ctk
from PIL import Image
import os

# =====================================================================
# 1. BANCO DE DADOS (CORRIGIDO PARA SALVAMENTO)
# =====================================================================

def conectar():
    return sqlite3.connect("estoque.db")

def criar_tabela():
    conexao = conectar()
    cursor = conexao.cursor()
    # Criando com a coluna padrão 'nome'
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
    # Inserindo na coluna correta
    cursor.execute("""
        INSERT INTO produtos (nome, quantidade, minimo)
        VALUES (?, ?, ?)
    """, (nome, quantidade, minimo))
    conexao.commit()
    conexao.close()

def listar_produtos(filtro_nome=""):
    conexao = conectar()
    cursor = conexao.cursor()
    if filtro_nome:
        cursor.execute("SELECT id, nome, quantidade, minimo FROM produtos WHERE nome LIKE ?", (f"%{filtro_nome}%",))
    else:
        cursor.execute("SELECT id, nome, quantidade, minimo FROM produtos")
    produtos = cursor.fetchall()
    conexao.close()
    return produtos

def deletar_produto(nome_produto):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM produtos WHERE nome = ?", (nome_produto,))
    conexao.commit()
    linhas_afetadas = cursor.rowcount
    conexao.close()
    return linhas_afetadas > 0


# =====================================================================
# 2. LÓGICA DAS TELAS E INTERAÇÕES
# =====================================================================

def abrir_gerenciador_estoque():
    """Esconde a tela inicial e abre a janela do estoque."""
    tela_inicial.withdraw() 
    construir_tela_estoque() 

def voltar_para_menu(janela_atual):
    """Fecha a janela do estoque e traz a tela inicial de volta."""
    janela_atual.destroy()
    tela_inicial.deiconify()

def atualizar_lista_na_tela(filtro=""):
    """Busca as informações no banco e desenha adicionando o Alerta de Estoque Baixo"""
    caixa_lista.configure(state="normal")
    caixa_lista.delete("0.0", "end")
    
    caixa_lista.insert("end", f"{'Nº':<5} | {'PRODUTO':<25} | {'QTD':<10} | {'MÍNIMO':<10} | {'STATUS':<15}\n")
    caixa_lista.insert("end", "-" * 75 + "\n")
    
    produtos = listar_produtos(filtro)
    
    contador_visual = 1
    for prod in produtos:
        id_prod, nome, qtd, min_est = prod
        
        if qtd <= min_est:
            status = "⚠️ REABASTECER"
        else:
            status = "✅ OK"
            
        caixa_lista.insert("end", f"{contador_visual:<5} | {nome:<25} | {qtd:<10} | {min_est:<10} | {status:<15}\n")
        contador_visual += 1
    
    caixa_lista.configure(state="disabled")

def filtrar_pesquisa(evento):
    texto_busca = entrada_pesquisa.get()
    atualizar_lista_na_tela(texto_busca)

def acao_botao_cadastrar():
    nome = entrada_produto.get()
    txt_quantidade = entrada_quantidade.get()
    txt_minimo = entrada_minimo.get()
    
    if nome == "" or txt_quantidade == "" or txt_minimo == "":
        label_status.configure(text="Erro: Preencha todos os campos!", text_color="red")
        return

    try:
        quantidade = int(txt_quantidade)
        minimo = int(txt_minimo)
        
        adicionar_produto(nome=nome, quantidade=quantidade, minimo=minimo)
        
        label_status.configure(text=f"'{nome}' cadastrado com sucesso!", text_color="green")
        atualizar_lista_na_tela()
        
        entrada_produto.delete(0, 'end')
        entrada_quantidade.delete(0, 'end')
        entrada_minimo.delete(0, 'end')
        
    except ValueError:
        label_status.configure(text="Erro: Quantidade e Mínimo devem ser apenas números!", text_color="red")

def acao_botao_excluir():
    nome_prod = entrada_excluir.get()
    if nome_prod == "":
        label_status.configure(text="Erro: Digite o NOME do produto para excluir!", text_color="red")
        return
    
    if deletar_produto(nome_prod):
        label_status.configure(text=f"Produto '{nome_prod}' excluído com sucesso!", text_color="green")
        atualizar_lista_na_tela()
        entrada_excluir.delete(0, 'end')
    else:
        label_status.configure(text="Erro: Produto não encontrado! Verifique se digitou corretamente.", text_color="red")


# =====================================================================
# 3. CONSTRUÇÃO DA INTERFACE DO ESTOQUE (JANELA PRINCIPAL)
# =====================================================================

def construir_tela_estoque():
    global entrada_produto, entrada_quantidade, entrada_minimo, botao_cadastrar
    global label_status, caixa_lista, entrada_pesquisa, entrada_excluir
    
    tela_estoque = ctk.CTkToplevel() 
    tela_estoque.title("LIMETAL - Controle de Estoque")
    tela_estoque.state('zoomed') 
    
    tela_estoque.protocol("WM_DELETE_WINDOW", tela_inicial.destroy)
    
    frame_topo = ctk.CTkFrame(tela_estoque, fg_color="transparent")
    frame_topo.pack(pady=10, fill="x", padx=20)
    
    botao_voltar = ctk.CTkButton(frame_topo, text="⬅ Voltar", width=80, fg_color="#444444", hover_color="#222222", command=lambda: voltar_para_menu(tela_estoque))
    botao_voltar.pack(side="left")
    
    titulo = ctk.CTkLabel(frame_topo, text="Painel de Controle de Estoque", font=("Arial", 20, "bold"))
    titulo.pack(side="left", padx=40)
    
    frame_cadastro = ctk.CTkFrame(tela_estoque)
    frame_cadastro.pack(pady=10, fill="x", padx=20, ipadx=10, ipady=10)
    
    ctk.CTkLabel(frame_cadastro, text="Nome do Produto:").pack()
    entrada_produto = ctk.CTkEntry(frame_cadastro, width=350)
    entrada_produto.pack(pady=2)
    
    ctk.CTkLabel(frame_cadastro, text="Quantidade:").pack()
    entrada_quantidade = ctk.CTkEntry(frame_cadastro, width=350)
    entrada_quantidade.pack(pady=2)
    
    ctk.CTkLabel(frame_cadastro, text="Estoque Mínimo:").pack()
    entrada_minimo = ctk.CTkEntry(frame_cadastro, width=350)
    entrada_minimo.pack(pady=2)
    
    botao_cadastrar = ctk.CTkButton(frame_cadastro, text="Cadastrar Item", command=acao_botao_cadastrar)
    botao_cadastrar.pack(pady=10)
    
    label_status = ctk.CTkLabel(tela_estoque, text="", font=("Arial", 12))
    label_status.pack()
    
    frame_busca = ctk.CTkFrame(tela_estoque)
    frame_busca.pack(pady=5, fill="x", padx=20)
    
    ctk.CTkLabel(frame_busca, text="🔍 Buscar produto:", font=("Arial", 12, "bold")).pack(side="left", padx=10, pady=5)
    entrada_pesquisa = ctk.CTkEntry(frame_busca, width=250, placeholder_text="Digite o nome...")
    entrada_pesquisa.pack(side="right", padx=10, pady=5)
    entrada_pesquisa.bind("<KeyRelease>", filtrar_pesquisa) 
    
    caixa_lista = ctk.CTkTextbox(tela_estoque, width=600, height=220, font=("Courier New", 12))
    caixa_lista.pack(pady=10, fill="both", expand=True, padx=20)
    
    frame_excluir = ctk.CTkFrame(tela_estoque)
    frame_excluir.pack(pady=10, fill="x", padx=20)
    
    ctk.CTkLabel(frame_excluir, text="Excluir por Nome:").pack(side="left", padx=10)
    entrada_excluir = ctk.CTkEntry(frame_excluir, width=250, placeholder_text="Ex: Tubo 20x20")
    entrada_excluir.pack(side="left", padx=5)
    
    botao_excluir = ctk.CTkButton(frame_excluir, text="Apagar Produto", fg_color="red", hover_color="#990000", command=acao_botao_excluir)
    botao_excluir.pack(side="right", padx=10, pady=5)
    
    atualizar_lista_na_tela()

# =====================================================================
# 4. TELA INICIAL
# =====================================================================

criar_tabela()

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

tela_inicial = ctk.CTk()
tela_inicial.title("LIMETAL - Painel Administrativo")
tela_inicial.state('zoomed') 

caminho_logo = "logotipo.jpeg"

if os.path.exists(caminho_logo):
    imagem_aberta = Image.open(caminho_logo)
    
    largura_tela = tela_inicial.winfo_screenwidth()
    altura_tela = tela_inicial.winfo_screenheight()
    
    proporcao_foto = imagem_aberta.width / imagem_aberta.height
    proporcao_tela = largura_tela / altura_tela
    
    if proporcao_foto > proporcao_tela:
        nova_altura = altura_tela
        nova_largura = int(altura_tela * proporcao_foto)
    else:
        nova_largura = largura_tela
        nova_altura = int(largura_tela / proporcao_foto)
        
    imagem_redimensionada = imagem_aberta.resize((nova_largura, nova_altura), Image.Resampling.LANCZOS)
    
    esquerda = (nova_largura - largura_tela) / 2
    topo = (nova_altura - altura_tela) / 2
    direita = esquerda + largura_tela
    fundo = topo + altura_tela
    
    imagem_final = imagem_redimensionada.crop((esquerda, topo, direita, fundo))
    
    logo_img = ctk.CTkImage(
        light_image=imagem_final, 
        dark_image=imagem_final, 
        size=(largura_tela, altura_tela)
    )
    
    label_imagem = ctk.CTkLabel(tela_inicial, image=logo_img, text="")
    label_imagem.pack(fill="both", expand=True)
    
    btn_entrar = ctk.CTkButton(
        tela_inicial, 
        text="ABRIR SISTEMA DE ESTOQUE", 
        font=("Arial", 16, "bold"), 
        fg_color="#1063a3",       
        hover_color="#0b4674",    
        height=55, 
        width=400,                
        corner_radius=10,         
        command=abrir_gerenciador_estoque
    )
    btn_entrar.place(relx=0.5, rely=0.73, anchor="center") 

    btn_sair = ctk.CTkButton(
        tela_inicial, 
        text="SAIR DO PROGRAMA", 
        font=("Arial", 14, "bold"), 
        fg_color="#09437a",       
        hover_color="#062e54",    
        height=50, 
        width=400,
        corner_radius=10,
        command=tela_inicial.destroy
    )
    btn_sair.place(relx=0.5, rely=0.83, anchor="center")

else:
    label_alternativo = ctk.CTkLabel(
        tela_inicial, 
        text="LIMETAL\nEstruturas Metálicas", 
        font=("Arial", 48, "bold"),
        text_color="#ffffff"
    )
    label_alternativo.pack(expand=True)

tela_inicial.mainloop()