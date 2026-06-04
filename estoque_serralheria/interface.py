import sqlite3
import customtkinter as ctk
from PIL import Image
import os
import platform
from datetime import datetime

# =====================================================================
# 1. BANCO DE DADOS
# =====================================================================

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

def editar_produto(nome_produto, nova_quantidade, novo_minimo):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        UPDATE produtos 
        SET quantidade = ?, minimo = ? 
        WHERE nome = ?
    """, (nova_quantidade, novo_minimo, nome_produto))
    conexao.commit()
    linhas_afetadas = cursor.rowcount
    conexao.close()
    return linhas_afetadas > 0


# =====================================================================
# 2. MOTOR DE GERAÇÃO DO RELATÓRIO PDF (API REPORTLAB - OTIMIZADA)
# =====================================================================

def gerar_pdf_estoque():
    """Lê o banco de dados e gera um arquivo PDF profissional formatado sem travar."""
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.platypus import SimpleDocTemplate, Spacer, Table, TableStyle
        from reportlab.lib import colors
        
        nome_arquivo = "relatorio_estoque_limetal.pdf"
        
        doc = SimpleDocTemplate(nome_arquivo, pagesize=A4, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
        elementos = []
        
        data_hora = datetime.now().strftime("%d/%m/%Y as %H:%M:%S")
        dados_cabecalho = [
            ["LIMETAL - ESTRUTURAS METALICAS"],
            ["RELATORIO GERENCIAL DE ESTOQUE"],
            [f"Gerado em: {data_hora}"]
        ]
        
        tabela_cabecalho = Table(dados_cabecalho, colWidths=[510])
        tabela_cabecalho.setStyle(TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('FONTNAME', (0,0), (0,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (0,0), 18),
            ('TEXTCOLOR', (0,0), (0,0), colors.HexColor("#1063a3")),
            ('FONTNAME', (0,1), (0,1), 'Helvetica-Bold'),
            ('FONTSIZE', (0,1), (0,1), 12),
            ('TEXTCOLOR', (0,1), (0,1), colors.HexColor("#444444")),
            ('FONTSIZE', (0,2), (0,2), 9),
            ('TEXTCOLOR', (0,2), (0,2), colors.HexColor("#777777")),
            ('BOTTOMPADDING', (0,2), (0,2), 15)
        ]))
        elementos.append(tabela_cabecalho)
        elementos.append(Spacer(1, 15))
        
        produtos = listar_produtos()
        dados_tabela = [["N*", "Nome do Produto", "Qtd. Atual", "Estoque Minimo", "Status"]]
        
        contador = 1
        for prod in produtos:
            id_prod, nome, qtd, min_est = prod
            status = "REABASTECER" if qtd <= min_est else "OK"
            dados_tabela.append([str(contador), str(nome), str(qtd), str(min_est), status])
            contador += 1
            
        tabela_pdf = Table(dados_tabela, colWidths=[35, 230, 80, 85, 80])
        
        estilo_tabela = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1063a3")), 
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('ALIGN', (1, 1), (1, -1), 'LEFT'), 
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor("#f9f9f9")), 
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#dddddd")), 
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ])
        
        for i in range(1, len(dados_tabela)):
            if dados_tabela[i][4] == "REABASTECER":
                estilo_tabela.add('TEXTCOLOR', (4, i), (4, i), colors.HexColor("#cc0000")) 
                estilo_tabela.add('FONTNAME', (4, i), (4, i), 'Helvetica-Bold')
            else:
                estilo_tabela.add('TEXTCOLOR', (4, i), (4, i), colors.HexColor("#008800")) 
        
        tabela_pdf.setStyle(estilo_tabela)
        elementos.append(tabela_pdf)
        
        doc.build(elementos)
        return True
    except Exception as erro:
        print("Erro detalhado do ReportLab:", erro)
        return False


# =====================================================================
# 3. LOGICA DAS TELAS E INTERAÇÕES
# =====================================================================

def abrir_gerenciador_estoque():
    tela_inicial.withdraw() 
    construir_tela_estoque() 

def voltar_para_menu(janela_atual):
    janela_atual.destroy()
    tela_inicial.deiconify()

def atualizar_lista_na_tela(filtro=""):
    caixa_lista.configure(state="normal")
    caixa_lista.delete("0.0", "end")
    
    caixa_lista.insert("end", f"{'N*':<5} | {'PRODUTO':<25} | {'QTD':<10} | {'MINIMO':<10} | {'STATUS':<15}\n")
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
        
        # Corrigido aqui: Removida a linha duplicada com erro
        adicionar_produto(nome=nome, quantidade=quantidade, minimo=minimo)
        
        label_status.configure(text=f"'{nome}' cadastrado com sucesso!", text_color="green")
        atualizar_lista_na_tela()
        
        entrada_produto.delete(0, 'end')
        entrada_quantidade.delete(0, 'end')
        entrada_minimo.delete(0, 'end')
        
    except ValueError:
        label_status.configure(text="Erro: Quantidade e Minimo devem ser apenas numeros!", text_color="red")

def acao_botao_excluir():
    nome_prod = entrada_excluir.get()
    if nome_prod == "":
        label_status.configure(text="Erro: Digite o NOME do produto para excluir!", text_color="red")
        return
    
    if deletar_produto(nome_prod):
        label_status.configure(text=f"Produto '{nome_prod}' excluido com sucesso!", text_color="green")
        atualizar_lista_na_tela()
        entrada_excluir.delete(0, 'end')
    else:
        label_status.configure(text="Erro: Produto nao encontrado!", text_color="red")

def acao_botao_editar():
    nome_prod = entrada_edit_nome.get()
    txt_qtd = entrada_edit_qtd.get()
    txt_min = entrada_edit_min.get()
    
    if nome_prod == "" or txt_qtd == "" or txt_min == "":
        label_status.configure(text="Erro: Preencha Nome, Nova Qtd e Novo Minimo para editar!", text_color="red")
        return
        
    try:
        nova_qtd = int(txt_qtd)
        novo_min = int(txt_min)
        
        if editar_produto(nome_prod, nova_qtd, novo_min):
            label_status.configure(text=f"Produto '{nome_prod}' atualizado com sucesso!", text_color="green")
            atualizar_lista_na_tela()
            entrada_edit_nome.delete(0, 'end')
            entrada_edit_qtd.delete(0, 'end')
            entrada_edit_min.delete(0, 'end')
        else:
            label_status.configure(text="Erro: Produto nao encontrado para edicao!", text_color="red")
            
    except ValueError:
        label_status.configure(text="Erro: Nova Qtd e Novo Minimo devem ser numeros!", text_color="red")

def acao_gerar_pdf():
    if gerar_pdf_estoque():
        label_status.configure(text="📋 PDF criado com sucesso e aberto na tela!", text_color="green")
        
        nome_arquivo = "relatorio_estoque_limetal.pdf"
        try:
            if platform.system() == "Windows":
                os.startfile(nome_arquivo)
            elif platform.system() == "Darwin":
                os.system(f"open {nome_arquivo}")
            else:
                os.system(f"xdg-open {nome_arquivo}")
        except Exception as e:
            print("Nao foi possivel abrir o PDF automaticamente:", e)
    else:
        label_status.configure(text="❌ Erro ao gerar PDF. Verifique se o arquivo nao esta aberto.", text_color="red")


# =====================================================================
# 4. CONSTRUÇÃO DA INTERFACE DO ESTOQUE
# =====================================================================

def construir_tela_estoque():
    global entrada_produto, entrada_quantidade, entrada_minimo, botao_cadastrar
    global label_status, caixa_lista, entrada_pesquisa, entrada_excluir
    global entrada_edit_nome, entrada_edit_qtd, entrada_edit_min
    
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
    
    botao_pdf = ctk.CTkButton(frame_topo, text="📋 Exportar para PDF", font=("Arial", 12, "bold"), fg_color="#2cb742", hover_color="#218c32", width=150, command=acao_gerar_pdf)
    botao_pdf.pack(side="right")
    
    frame_cadastro = ctk.CTkFrame(tela_estoque)
    frame_cadastro.pack(pady=10, fill="x", padx=20, ipadx=10, ipady=10)
    
    ctk.CTkLabel(frame_cadastro, text="Nome do Produto:").pack()
    entrada_produto = ctk.CTkEntry(frame_cadastro, width=350)
    entrada_produto.pack(pady=2)
    
    ctk.CTkLabel(frame_cadastro, text="Quantidade:").pack()
    entrada_quantidade = ctk.CTkEntry(frame_cadastro, width=350)
    entrada_quantidade.pack(pady=2)
    
    ctk.CTkLabel(frame_cadastro, text="Estoque Minimo:").pack()
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
    
    frame_operacoes = ctk.CTkFrame(tela_estoque, fg_color="transparent")
    frame_operacoes.pack(pady=10, fill="x", padx=20)
    
    frame_excluir = ctk.CTkFrame(frame_operacoes)
    frame_excluir.pack(side="left", fill="both", expand=True, padx=(0, 10))
    
    ctk.CTkLabel(frame_excluir, text="❌ Excluir por Nome:", font=("Arial", 12, "bold")).pack(anchor="w", padx=10, pady=5)
    entrada_excluir = ctk.CTkEntry(frame_excluir, placeholder_text="Ex: Tubo 20x20")
    entrada_excluir.pack(fill="x", padx=10, pady=5)
    
    botao_excluir = ctk.CTkButton(frame_excluir, text="Apagar Produto", fg_color="red", hover_color="#990000", command=acao_botao_excluir)
    botao_excluir.pack(pady=10)
    
    frame_editar = ctk.CTkFrame(frame_operacoes)
    frame_editar.pack(side="right", fill="both", expand=True, padx=(10, 0))
    
    ctk.CTkLabel(frame_editar, text="✏️ Editar Produto Existente:", font=("Arial", 12, "bold")).pack(anchor="w", padx=10, pady=5)
    
    sub_frame_edit = ctk.CTkFrame(frame_editar, fg_color="transparent")
    sub_frame_edit.pack(fill="x", padx=10)
    
    entrada_edit_nome = ctk.CTkEntry(sub_frame_edit, placeholder_text="Nome do Produto", width=180)
    entrada_edit_nome.pack(side="left", padx=2, expand=True, fill="x")
    
    entrada_edit_qtd = ctk.CTkEntry(sub_frame_edit, placeholder_text="Nova Qtd", width=90)
    entrada_edit_qtd.pack(side="left", padx=2, expand=True, fill="x")
    
    entrada_edit_min = ctk.CTkEntry(sub_frame_edit, placeholder_text="Novo Min.", width=90)
    entrada_edit_min.pack(side="left", padx=2, expand=True, fill="x")
    
    botao_editar = ctk.CTkButton(frame_editar, text="Salvar Alterações", fg_color="#1063a3", hover_color="#0b4674", command=acao_botao_editar)
    botao_editar.pack(pady=10)
    
    atualizar_lista_na_tela()

# =====================================================================
# 5. TELA INICIAL
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
    
    logo_img = ctk.CTkImage(light_image=imagem_final, dark_image=imagem_final, size=(largura_tela, altura_tela))
    
    label_imagem = ctk.CTkLabel(tela_inicial, image=logo_img, text="")
    label_imagem.pack(fill="both", expand=True)
    
    btn_entrar = ctk.CTkButton(tela_inicial, text="ABRIR SISTEMA DE ESTOQUE", font=("Arial", 16, "bold"), fg_color="#1063a3", hover_color="#0b4674", height=55, width=400, corner_radius=10, command=abrir_gerenciador_estoque)
    btn_entrar.place(relx=0.5, rely=0.73, anchor="center") 

    btn_sair = ctk.CTkButton(tela_inicial, text="SAIR DO PROGRAMA", font=("Arial", 14, "bold"), fg_color="#09437a", hover_color="#062e54", height=50, width=400, corner_radius=10, command=tela_inicial.destroy)
    btn_sair.place(relx=0.5, rely=0.83, anchor="center")
else:
    label_alternativo = ctk.CTkLabel(tela_inicial, text="LIMETAL\nEstruturas Metalicas", font=("Arial", 48, "bold"), text_color="#ffffff")
    label_alternativo.pack(expand=True)

tela_inicial.mainloop()