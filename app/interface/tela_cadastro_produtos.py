import tkinter as tk
from tkinter import messagebox, ttk
from app.db.db_manager import DBManager
from app.interface.tela_cadastro_fornecedores import TelaCadastroFornecedor
import logging


class TelaCadastroProduto(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Cadastro de Produto")
        self.geometry("600x600")
        self.db = master.db if hasattr(master, 'db') else DBManager()

        self.fornecedor_selecionado = None
        self.criar_widgets()
        self.carregar_fornecedores()
        self.protocol("WM_DELETE_WINDOW", self.fechar_janela)

    def criar_widgets(self):
        main_frame = tk.Frame(self)
        main_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        # Frame para dados do produto
        produto_frame = tk.LabelFrame(main_frame, text="Dados do Produto", padx=10, pady=10)
        produto_frame.pack(fill=tk.X, pady=5)

        tk.Label(produto_frame, text="Nome*:").grid(row=0, column=0, sticky="e", pady=5)
        self.entry_nome = tk.Entry(produto_frame, width=40)
        self.entry_nome.grid(row=0, column=1)

        tk.Label(produto_frame, text="Código*:").grid(row=1, column=0, sticky="e", pady=5)
        self.entry_codigo = tk.Entry(produto_frame, width=40)
        self.entry_codigo.grid(row=1, column=1)

        tk.Label(produto_frame, text="Descrição:").grid(row=2, column=0, sticky="e", pady=5)
        self.entry_descricao = tk.Entry(produto_frame, width=40)
        self.entry_descricao.grid(row=2, column=1)

        tk.Label(produto_frame, text="Categoria:").grid(row=3, column=0, sticky="e", pady=5)
        self.entry_categoria = tk.Entry(produto_frame, width=40)
        self.entry_categoria.grid(row=3, column=1)

        tk.Label(produto_frame, text="Preço de Custo:").grid(row=4, column=0, sticky="e", pady=5)
        self.entry_preco_custo = tk.Entry(produto_frame, width=40)
        self.entry_preco_custo.grid(row=4, column=1)

        tk.Label(produto_frame, text="Preço de Venda:").grid(row=5, column=0, sticky="e", pady=5)
        self.entry_preco_venda = tk.Entry(produto_frame, width=40)
        self.entry_preco_venda.grid(row=5, column=1)

        tk.Label(produto_frame, text="Estoque Mínimo:").grid(row=6, column=0, sticky="e", pady=5)
        self.entry_estoque_minimo = tk.Entry(produto_frame, width=40)
        self.entry_estoque_minimo.grid(row=6, column=1)

        # Frame para seleção de fornecedor
        fornecedor_frame = tk.LabelFrame(main_frame, text="Fornecedor*", padx=10, pady=10)
        fornecedor_frame.pack(fill=tk.X, pady=10)

        # Treeview para listar fornecedores
        self.tree_fornecedores = ttk.Treeview(fornecedor_frame, columns=('id', 'nome', 'contato'), show='headings',
                                              height=5)
        self.tree_fornecedores.heading('id', text='ID')
        self.tree_fornecedores.heading('nome', text='Nome')
        self.tree_fornecedores.heading('contato', text='Contato')
        self.tree_fornecedores.column('id', width=50, anchor='center')
        self.tree_fornecedores.column('nome', width=150)
        self.tree_fornecedores.column('contato', width=100)

        scroll = ttk.Scrollbar(fornecedor_frame, orient="vertical", command=self.tree_fornecedores.yview)
        self.tree_fornecedores.configure(yscrollcommand=scroll.set)

        self.tree_fornecedores.grid(row=0, column=0, sticky='nsew')
        scroll.grid(row=0, column=1, sticky='ns')

        # Bind para seleção de fornecedor
        self.tree_fornecedores.bind('<<TreeviewSelect>>', self.selecionar_fornecedor)

        # Botões para fornecedor
        btn_fornecedor_frame = tk.Frame(fornecedor_frame)
        btn_fornecedor_frame.grid(row=1, column=0, columnspan=2, pady=5)

        tk.Button(btn_fornecedor_frame, text="Novo Fornecedor", command=self.abrir_cadastro_fornecedor).pack(
            side=tk.LEFT, padx=5)
        tk.Button(btn_fornecedor_frame, text="Atualizar Lista", command=self.carregar_fornecedores).pack(side=tk.LEFT,
                                                                                                         padx=5)

        # Label para mostrar fornecedor selecionado
        self.lbl_fornecedor_selecionado = tk.Label(fornecedor_frame, text="Nenhum fornecedor selecionado", fg='red')
        self.lbl_fornecedor_selecionado.grid(row=2, column=0, columnspan=2, pady=5)

        # Frame para botões de ação
        btn_frame = tk.Frame(main_frame)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Cadastrar", command=self.cadastrar).pack(side=tk.RIGHT, padx=10)
        tk.Button(btn_frame, text="Cancelar", command=self.fechar_janela).pack(side=tk.LEFT, padx=10)

    def carregar_fornecedores(self):
        try:
            # Limpa a treeview
            for item in self.tree_fornecedores.get_children():
                self.tree_fornecedores.delete(item)

            # Carrega os fornecedores do banco de dados
            fornecedores = self.db.listar_fornecedores()

            # Adiciona cada fornecedor na treeview
            for fornecedor in fornecedores:
                self.tree_fornecedores.insert('', 'end', values=(fornecedor[0], fornecedor[1], fornecedor[2]))

        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao carregar fornecedores: {str(e)}")
            logging.error(f"Erro ao carregar fornecedores: {str(e)}", exc_info=True)

    def selecionar_fornecedor(self, event):
        selected_item = self.tree_fornecedores.selection()
        if selected_item:
            item = self.tree_fornecedores.item(selected_item[0])
            self.fornecedor_selecionado = item['values'][0]  # Pega o ID do fornecedor
            self.lbl_fornecedor_selecionado.config(
                text=f"Fornecedor selecionado: {item['values'][1]} (ID: {item['values'][0]})",
                fg='green'
            )

    def abrir_cadastro_fornecedor(self):
        TelaCadastroFornecedor(self)
        # Após cadastrar, atualiza a lista de fornecedores
        self.after(500, self.carregar_fornecedores)

    def cadastrar(self):
        try:
            nome = self.entry_nome.get().strip()
            codigo = self.entry_codigo.get().strip()
            descricao = self.entry_descricao.get().strip()
            categoria = self.entry_categoria.get().strip()

            try:
                preco_custo = float(self.entry_preco_custo.get() or 0)
                preco_venda = float(self.entry_preco_venda.get() or 0)
                estoque_minimo = int(self.entry_estoque_minimo.get() or 0)
            except ValueError:
                raise ValueError("Valores numéricos inválidos")

            if not nome or not codigo:
                raise ValueError("Nome e código são obrigatórios")

            if not self.fornecedor_selecionado:
                raise ValueError("Selecione um fornecedor para o produto")

            produto_id = self.db.inserir_produto(
                nome=nome,
                codigo=codigo,
                descricao=descricao,
                categoria=categoria,
                fornecedor_id=self.fornecedor_selecionado,
                quantidade=0,
                estoque_minimo=estoque_minimo,
                preco_custo=preco_custo,
                preco_venda=preco_venda
            )

            messagebox.showinfo("Sucesso", f"Produto cadastrado com sucesso!\nID: {produto_id}")
            self.fechar_janela()

        except ValueError as e:
            messagebox.showwarning("Atenção", str(e))
        except Exception as e:
            messagebox.showerror("Erro", f"Falha no cadastro: {str(e)}")
            logging.error(f"Erro no cadastro de produto: {str(e)}", exc_info=True)

    def fechar_janela(self):
        try:
            if hasattr(self, 'db') and self.db != getattr(self.master, 'db', None):
                self.db.fechar()
            self.destroy()
        except Exception as e:
            logging.error(f"Erro ao fechar janela: {str(e)}")
            self.destroy()