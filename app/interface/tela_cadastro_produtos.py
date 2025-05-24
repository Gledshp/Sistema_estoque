import tkinter as tk
from tkinter import messagebox, ttk
from app.db.db_manager import DBManager
from app.interface.tela_cadastro_fornecedores import TelaCadastroFornecedores

class TelaCadastroProdutos(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Cadastro de Produtos")
        self.geometry("800x800")
        self.resizable(False, False)

        self.db = DBManager()

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

        btn_cadastrar = tk.Button(self, text="Cadastrar Produto", command=self.cadastrar_produto)
        btn_cadastrar.pack(pady=10)

        btn_cadastrar_fornecedor = tk.Button(self, text="Cadastrar Fornecedor", command=self.cadastrar_fornecedor)
        btn_cadastrar_fornecedor.pack(pady=5)

    def atualizar_fornecedores(self):
        fornecedores = self.db.listar_fornecedores()
        nomes = [f[1] for f in fornecedores]  # Assuming id, nome, contato...
        self.combo_fornecedor['values'] = nomes
        if nomes:
            self.combo_fornecedor.current(0)

    def cadastrar_produto(self):
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
        fornecedores = self.db.listar_fornecedores()
        for f in fornecedores:
            if f[1] == fornecedor_nome:
                fornecedor_id = f[0]
                break

        try:
            self.db.inserir_produto(
                nome, codigo, descricao, categoria, fornecedor_id,
                quantidade, estoque_minimo, preco_custo, preco_venda
            )
            messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso")
            self.destroy()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao cadastrar produto: {e}")

    def cadastrar_fornecedor(self):
        self.withdraw()
        tela = TelaCadastroFornecedores(self)
        tela.wait_window()
        self.atualizar_fornecedores()
        self.deiconify()
