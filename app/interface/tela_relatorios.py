import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from app.db.db_manager import DBManager


class TelaRelatorios(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Relatórios")
        self.geometry("900x600")
        self.resizable(True, True)

        self.db = DBManager()

        self.criar_widgets()

    def criar_widgets(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.aba_produtos = ttk.Frame(self.notebook)
        self.notebook.add(self.aba_produtos, text="Produtos")

        # Treeview para produtos
        self.tree_produtos = ttk.Treeview(self.aba_produtos, columns=(
            "nome", "codigo", "categoria", "quantidade", "estoque_minimo",
            "preco_custo", "preco_venda", "fornecedor"
        ), show="headings")

        self.tree_produtos.heading("nome", text="Nome")
        self.tree_produtos.heading("codigo", text="Código")
        self.tree_produtos.heading("categoria", text="Categoria")
        self.tree_produtos.heading("quantidade", text="Quantidade")
        self.tree_produtos.heading("estoque_minimo", text="Estoque Mínimo")
        self.tree_produtos.heading("preco_custo", text="Preço Custo")
        self.tree_produtos.heading("preco_venda", text="Preço Venda")
        self.tree_produtos.heading("fornecedor", text="Fornecedor")

        self.tree_produtos.column("nome", width=150)
        self.tree_produtos.column("codigo", width=80)
        self.tree_produtos.column("categoria", width=100)
        self.tree_produtos.column("quantidade", width=80)
        self.tree_produtos.column("estoque_minimo", width=80)
        self.tree_produtos.column("preco_custo", width=80)
        self.tree_produtos.column("preco_venda", width=80)
        self.tree_produtos.column("fornecedor", width=150)

        scroll_produtos = ttk.Scrollbar(self.aba_produtos, orient="vertical", command=self.tree_produtos.yview)
        self.tree_produtos.configure(yscrollcommand=scroll_produtos.set)
        scroll_produtos.pack(side="right", fill="y")
        self.tree_produtos.pack(fill=tk.BOTH, expand=True)
        self.aba_fornecedores = ttk.Frame(self.notebook)
        self.notebook.add(self.aba_fornecedores, text="Fornecedores")
        self.tree_fornecedores = ttk.Treeview(self.aba_fornecedores, columns=(
            "nome", "contato", "telefone", "email", "total_produtos"
        ), show="headings")

        self.tree_fornecedores.heading("nome", text="Nome")
        self.tree_fornecedores.heading("contato", text="Contato")
        self.tree_fornecedores.heading("telefone", text="Telefone")
        self.tree_fornecedores.heading("email", text="Email")
        self.tree_fornecedores.heading("total_produtos", text="Total Produtos")

        self.tree_fornecedores.column("nome", width=150)
        self.tree_fornecedores.column("contato", width=120)
        self.tree_fornecedores.column("telefone", width=100)
        self.tree_fornecedores.column("email", width=150)
        self.tree_fornecedores.column("total_produtos", width=80)

        scroll_fornecedores = ttk.Scrollbar(self.aba_fornecedores, orient="vertical",
                                            command=self.tree_fornecedores.yview)
        self.tree_fornecedores.configure(yscrollcommand=scroll_fornecedores.set)
        scroll_fornecedores.pack(side="right", fill="y")
        self.tree_fornecedores.pack(fill=tk.BOTH, expand=True)

        # Botão para carregar dados
        btn_carregar = tk.Button(self, text="Carregar Relatórios", command=self.carregar_dados)
        btn_carregar.pack(pady=10)
        self.carregar_dados()

    def carregar_dados(self):
        for item in self.tree_produtos.get_children():
            self.tree_produtos.delete(item)

        for item in self.tree_fornecedores.get_children():
            self.tree_fornecedores.delete(item)

        # Carrega dados de produtos
        produtos = self.db.gerar_relatorio_produtos()
        for produto in produtos:
            self.tree_produtos.insert("", "end", values=produto)

        # Carrega dados de fornecedores
        fornecedores = self.db.gerar_relatorio_fornecedores()
        for fornecedor in fornecedores:
            self.tree_fornecedores.insert("", "end", values=fornecedor)