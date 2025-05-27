# app/interface/tela_principal.py
import tkinter as tk
from tkinter import messagebox, ttk
from app.interface.tela_cadastro_usuarios import TelaCadastroUsuarios
from app.interface.tela_cadastro_fornecedores import TelaCadastroFornecedores
from app.interface.tela_cadastro_produtos import TelaCadastroProdutos
from app.interface.tela_edicao_produtos import TelaEdicaoProdutos
from app.interface.tela_edicao_fornecedores import TelaEdicaoFornecedores
from app.interface.tela_relatorios import TelaRelatorios
from app.db.db_manager import DBManager

class TelaPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Estoque - Principal")
        self.geometry("800x600")
        self.resizable(False, False)

        self.db = DBManager()
        self.criar_widgets()

    def criar_widgets(self):
        # Frame principal
        main_frame = tk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Frame para cadastros
        frame_cadastros = tk.LabelFrame(main_frame, text="Cadastros", padx=10, pady=10)
        frame_cadastros.pack(fill=tk.X, pady=5)

        btn_usuarios = tk.Button(frame_cadastros, text="Cadastrar Usuário", width=20, command=self.cadastrar_usuario)
        btn_usuarios.pack(side=tk.LEFT, padx=5)

        btn_fornecedores = tk.Button(frame_cadastros, text="Cadastrar Fornecedor", width=20, command=self.cadastrar_fornecedor)
        btn_fornecedores.pack(side=tk.LEFT, padx=5)

        btn_produtos = tk.Button(frame_cadastros, text="Cadastrar Produto", width=20, command=self.cadastrar_produto)
        btn_produtos.pack(side=tk.LEFT, padx=5)

        # Frame para edições
        frame_edicoes = tk.LabelFrame(main_frame, text="Edições", padx=10, pady=10)
        frame_edicoes.pack(fill=tk.X, pady=5)

        btn_editar_produtos = tk.Button(frame_edicoes, text="Editar Produtos", width=20, command=self.editar_produtos)
        btn_editar_produtos.pack(side=tk.LEFT, padx=5)

        btn_editar_fornecedores = tk.Button(frame_edicoes, text="Editar Fornecedores", width=20, command=self.editar_fornecedores)
        btn_editar_fornecedores.pack(side=tk.LEFT, padx=5)

        # Frame para relatórios
        frame_relatorios = tk.LabelFrame(main_frame, text="Relatórios", padx=10, pady=10)
        frame_relatorios.pack(fill=tk.X, pady=5)

        btn_relatorios = tk.Button(frame_relatorios, text="Gerar Relatórios", width=20, command=self.gerar_relatorios)
        btn_relatorios.pack(side=tk.LEFT, padx=5)

        btn_estoque_baixo = tk.Button(frame_relatorios, text="Estoque Baixo", width=20, command=self.mostrar_estoque_baixo)
        btn_estoque_baixo.pack(side=tk.LEFT, padx=5)

        # Frame para sair
        frame_sair = tk.Frame(main_frame, padx=10, pady=10)
        frame_sair.pack(fill=tk.X, pady=5)

        btn_sair = tk.Button(frame_sair, text="Sair", width=20, command=self.quit)
        btn_sair.pack()

    def cadastrar_usuario(self):
        self.withdraw()
        tela = TelaCadastroUsuarios(self)
        tela.wait_window()
        self.deiconify()

    def cadastrar_fornecedor(self):
        self.withdraw()
        tela = TelaCadastroFornecedores(self)
        tela.wait_window()
        self.deiconify()

    def cadastrar_produto(self):
        self.withdraw()
        tela = TelaCadastroProdutos(self)
        tela.wait_window()
        self.deiconify()

    def editar_produtos(self):
        produtos = self.db.listar_produtos()
        if not produtos:
            messagebox.showinfo("Edição", "Nenhum produto cadastrado para editar.")
            return

        self.withdraw()
        tela_selecao = tk.Toplevel(self)
        tela_selecao.title("Selecionar Produto para Edição")
        tela_selecao.geometry("600x400")

        tk.Label(tela_selecao, text="Selecione o produto para editar:").pack(pady=10)

        tree = ttk.Treeview(tela_selecao, columns=("id", "nome", "codigo", "fornecedor"), show="headings")
        tree.heading("id", text="ID")
        tree.heading("nome", text="Nome")
        tree.heading("codigo", text="Código")
        tree.heading("fornecedor", text="Fornecedor")
        tree.column("id", width=50)
        tree.column("nome", width=200)
        tree.column("codigo", width=100)
        tree.column("fornecedor", width=200)

        for prod in produtos:
            tree.insert("", "end", values=(prod[0], prod[1], prod[2], prod[5]))

        scroll = ttk.Scrollbar(tela_selecao, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scroll.set)
        scroll.pack(side="right", fill="y")
        tree.pack(fill=tk.BOTH, expand=True)

        def on_select():
            selected_item = tree.focus()
            if not selected_item:
                return
            produto_id = tree.item(selected_item)["values"][0]
            tela_selecao.destroy()
            tela_edicao = TelaEdicaoProdutos(self, produto_id)
            tela_edicao.wait_window()
            self.deiconify()

        btn_selecionar = tk.Button(tela_selecao, text="Selecionar", command=on_select)
        btn_selecionar.pack(pady=10)

        tela_selecao.protocol("WM_DELETE_WINDOW", lambda: [tela_selecao.destroy(), self.deiconify()])

    def editar_fornecedores(self):
        fornecedores = self.db.listar_fornecedores()
        if not fornecedores:
            messagebox.showinfo("Edição", "Nenhum fornecedor cadastrado para editar.")
            return

        self.withdraw()
        tela_selecao = tk.Toplevel(self)
        tela_selecao.title("Selecionar Fornecedor para Edição")
        tela_selecao.geometry("600x400")

        tk.Label(tela_selecao, text="Selecione o fornecedor para editar:").pack(pady=10)

        tree = ttk.Treeview(tela_selecao, columns=("id", "nome", "contato", "telefone"), show="headings")
        tree.heading("id", text="ID")
        tree.heading("nome", text="Nome")
        tree.heading("contato", text="Contato")
        tree.heading("telefone", text="Telefone")
        tree.column("id", width=50)
        tree.column("nome", width=200)
        tree.column("contato", width=150)
        tree.column("telefone", width=100)

        for forn in fornecedores:
            tree.insert("", "end", values=(forn[0], forn[1], forn[2], forn[3]))

        scroll = ttk.Scrollbar(tela_selecao, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scroll.set)
        scroll.pack(side="right", fill="y")
        tree.pack(fill=tk.BOTH, expand=True)

        def on_select():
            selected_item = tree.focus()
            if not selected_item:
                return
            fornecedor_id = tree.item(selected_item)["values"][0]
            tela_selecao.destroy()
            tela_edicao = TelaEdicaoFornecedores(self, fornecedor_id)
            tela_edicao.wait_window()
            self.deiconify()

        btn_selecionar = tk.Button(tela_selecao, text="Selecionar", command=on_select)
        btn_selecionar.pack(pady=10)

        tela_selecao.protocol("WM_DELETE_WINDOW", lambda: [tela_selecao.destroy(), self.deiconify()])

    def gerar_relatorios(self):
        self.withdraw()
        tela = TelaRelatorios(self)
        tela.wait_window()
        self.deiconify()

    def mostrar_estoque_baixo(self):
        produtos = self.db.produtos_estoque_baixo()
        if not produtos:
            messagebox.showinfo("Estoque Baixo", "Nenhum produto está com estoque baixo.")
        else:
            msg = "Produtos com estoque baixo:\n"
            for nome, qtd, minimo in produtos:
                msg += f"{nome} - Qtde: {qtd}, Mínimo: {minimo}\n"
            messagebox.showwarning("Estoque Baixo", msg)