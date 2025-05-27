import tkinter as tk
from tkinter import messagebox, ttk
from app.db.db_manager import DBManager


class TelaEdicaoProdutos(tk.Toplevel):
    def __init__(self, master=None, produto_id=None):
        super().__init__(master)
        self.title("Edição de Produto")
        self.geometry("800x600")
        self.resizable(False, False)

        self.db = DBManager()
        self.produto_id = produto_id

        self.criar_widgets()
        self.carregar_dados_produto()

    def criar_widgets(self):
        tk.Label(self, text="Nome:").pack(pady=5)
        self.entry_nome = tk.Entry(self)
        self.entry_nome.pack()

        tk.Label(self, text="Código:").pack(pady=5)
        self.entry_codigo = tk.Entry(self)
        self.entry_codigo.pack()

        tk.Label(self, text="Descrição:").pack(pady=5)
        self.entry_descricao = tk.Entry(self)
        self.entry_descricao.pack()

        tk.Label(self, text="Categoria:").pack(pady=5)
        self.entry_categoria = tk.Entry(self)
        self.entry_categoria.pack()

        tk.Label(self, text="Fornecedor:").pack(pady=5)
        self.combo_fornecedor = ttk.Combobox(self, state="readonly")
        self.combo_fornecedor.pack()
        self.atualizar_fornecedores()

        tk.Label(self, text="Quantidade em estoque:").pack(pady=5)
        self.entry_quantidade = tk.Entry(self)
        self.entry_quantidade.pack()

        tk.Label(self, text="Estoque mínimo:").pack(pady=5)
        self.entry_estoque_minimo = tk.Entry(self)
        self.entry_estoque_minimo.pack()

        tk.Label(self, text="Preço de custo:").pack(pady=5)
        self.entry_preco_custo = tk.Entry(self)
        self.entry_preco_custo.pack()

        tk.Label(self, text="Preço de venda:").pack(pady=5)
        self.entry_preco_venda = tk.Entry(self)
        self.entry_preco_venda.pack()

        btn_salvar = tk.Button(self, text="Salvar Alterações", command=self.salvar_alteracoes)
        btn_salvar.pack(pady=10)

    def atualizar_fornecedores(self):
        fornecedores = self.db.listar_fornecedores()
        self.fornecedores_dict = {f[1]: f[0] for f in fornecedores}  # nome: id
        nomes = list(self.fornecedores_dict.keys())
        self.combo_fornecedor['values'] = nomes

    def carregar_dados_produto(self):
        if not self.produto_id:
            return

        produto = self.db.obter_produto_por_id(self.produto_id)
        if produto:
            self.entry_nome.insert(0, produto[1])
            self.entry_codigo.insert(0, produto[2])
            self.entry_descricao.insert(0, produto[3])
            self.entry_categoria.insert(0, produto[4])

            fornecedor_id = produto[5]
            if fornecedor_id:
                fornecedor = self.db.obter_fornecedor_por_id(fornecedor_id)
                if fornecedor:
                    self.combo_fornecedor.set(fornecedor[1])

            self.entry_quantidade.insert(0, str(produto[6]))
            self.entry_estoque_minimo.insert(0, str(produto[7]))
            self.entry_preco_custo.insert(0, str(produto[8]))
            self.entry_preco_venda.insert(0, str(produto[9]))

    def salvar_alteracoes(self):
        nome = self.entry_nome.get().strip()
        codigo = self.entry_codigo.get().strip()
        descricao = self.entry_descricao.get().strip()
        categoria = self.entry_categoria.get().strip()
        fornecedor_nome = self.combo_fornecedor.get()
        quantidade = self.entry_quantidade.get().strip()
        estoque_minimo = self.entry_estoque_minimo.get().strip()
        preco_custo = self.entry_preco_custo.get().strip()
        preco_venda = self.entry_preco_venda.get().strip()

        if not nome:
            messagebox.showwarning("Atenção", "Nome do produto é obrigatório")
            return

        try:
            quantidade = int(quantidade) if quantidade else 0
            estoque_minimo = int(estoque_minimo) if estoque_minimo else 0
            preco_custo = float(preco_custo) if preco_custo else 0.0
            preco_venda = float(preco_venda) if preco_venda else 0.0
        except ValueError:
            messagebox.showwarning("Atenção", "Quantidades e preços devem ser numéricos")
            return

        fornecedor_id = None
        if fornecedor_nome:
            fornecedor_id = self.fornecedores_dict.get(fornecedor_nome)

        try:
            self.db.atualizar_produto(
                self.produto_id, nome, codigo, descricao, categoria, fornecedor_id,
                quantidade, estoque_minimo, preco_custo, preco_venda
            )
            messagebox.showinfo("Sucesso", "Produto atualizado com sucesso")
            self.destroy()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao atualizar produto: {e}")