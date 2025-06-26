import tkinter as tk
from tkinter import messagebox, ttk
from app.db.db_manager import DBManager
from app.interface.tela_cadastro_fornecedores import TelaCadastroFornecedor
import logging
import re


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

        produto_frame = tk.LabelFrame(main_frame, text="Dados do Produto (* campos obrigatórios)", padx=10, pady=10)
        produto_frame.pack(fill=tk.X, pady=5)
        tk.Label(produto_frame, text="Nome*:").grid(row=0, column=0, sticky="e", pady=5)
        self.entry_nome = tk.Entry(produto_frame, width=40)
        self.entry_nome.grid(row=0, column=1, sticky="w")
        tk.Label(produto_frame, text="Código*:").grid(row=1, column=0, sticky="e", pady=5)
        self.entry_codigo = tk.Entry(produto_frame, width=40)
        self.entry_codigo.grid(row=1, column=1, sticky="w")
        tk.Label(produto_frame, text="Descrição*:").grid(row=2, column=0, sticky="e", pady=5)
        self.entry_descricao = tk.Entry(produto_frame, width=40)
        self.entry_descricao.grid(row=2, column=1, sticky="w")
        tk.Label(produto_frame, text="Categoria*:").grid(row=3, column=0, sticky="e", pady=5)
        self.entry_categoria = tk.Entry(produto_frame, width=40)
        self.entry_categoria.grid(row=3, column=1, sticky="w")

        valores_frame = tk.Frame(produto_frame)
        valores_frame.grid(row=4, column=0, columnspan=2, sticky="ew", pady=5)

        tk.Label(valores_frame, text="Preço de Custo*:").grid(row=0, column=0, sticky="e", padx=5)
        self.entry_preco_custo = tk.Entry(valores_frame, width=15)
        self.entry_preco_custo.grid(row=0, column=1, sticky="w")
        self.entry_preco_custo.bind('<KeyRelease>', lambda e: self.validar_numero(self.entry_preco_custo))
        tk.Label(valores_frame, text="R$").grid(row=0, column=2, sticky="w")

        tk.Label(valores_frame, text="Preço de Venda*:").grid(row=1, column=0, sticky="e", padx=5)
        self.entry_preco_venda = tk.Entry(valores_frame, width=15)
        self.entry_preco_venda.grid(row=1, column=1, sticky="w")
        self.entry_preco_venda.bind('<KeyRelease>', lambda e: self.validar_numero(self.entry_preco_venda))
        tk.Label(valores_frame, text="R$").grid(row=1, column=2, sticky="w")
        tk.Label(valores_frame, text="Estoque Mínimo*:").grid(row=2, column=0, sticky="e", padx=5)
        self.entry_estoque_minimo = tk.Entry(valores_frame, width=15)
        self.entry_estoque_minimo.grid(row=2, column=1, sticky="w")
        self.entry_estoque_minimo.bind('<KeyRelease>', lambda e: self.validar_inteiro(self.entry_estoque_minimo))
        tk.Label(valores_frame, text="unidades").grid(row=2, column=2, sticky="w")

        fornecedor_frame = tk.LabelFrame(main_frame, text="Fornecedor*", padx=10, pady=10)
        fornecedor_frame.pack(fill=tk.X, pady=10)
        self.tree_fornecedores = ttk.Treeview(fornecedor_frame,
                                              columns=('id', 'nome', 'contato'),
                                              show='headings',
                                              height=5)
        self.tree_fornecedores.heading('id', text='ID')
        self.tree_fornecedores.heading('nome', text='Nome')
        self.tree_fornecedores.heading('contato', text='Contato')
        self.tree_fornecedores.column('id', width=50, anchor='center')
        self.tree_fornecedores.column('nome', width=150, anchor='w')
        self.tree_fornecedores.column('contato', width=100, anchor='w')

        scroll = ttk.Scrollbar(fornecedor_frame,
                               orient="vertical",
                               command=self.tree_fornecedores.yview)
        self.tree_fornecedores.configure(yscrollcommand=scroll.set)

        self.tree_fornecedores.grid(row=0, column=0, sticky='nsew')
        scroll.grid(row=0, column=1, sticky='ns')

        fornecedor_frame.grid_columnconfigure(0, weight=1)

        self.tree_fornecedores.bind('<<TreeviewSelect>>', self.selecionar_fornecedor)

        btn_fornecedor_frame = tk.Frame(fornecedor_frame)
        btn_fornecedor_frame.grid(row=1, column=0, columnspan=2, pady=5)

        tk.Button(btn_fornecedor_frame,
                  text="Novo Fornecedor",
                  command=self.abrir_cadastro_fornecedor).pack(side=tk.LEFT, padx=5)

        tk.Button(btn_fornecedor_frame,
                  text="Atualizar Lista",
                  command=self.carregar_fornecedores).pack(side=tk.LEFT, padx=5)

        self.lbl_fornecedor_selecionado = tk.Label(fornecedor_frame,
                                                   text="Nenhum fornecedor selecionado",
                                                   fg='red')
        self.lbl_fornecedor_selecionado.grid(row=2, column=0, columnspan=2, pady=5)

        btn_frame = tk.Frame(main_frame)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame,
                  text="Cadastrar",
                  command=self.cadastrar).pack(side=tk.RIGHT, padx=10)

        tk.Button(btn_frame,
                  text="Cancelar",
                  command=self.fechar_janela).pack(side=tk.LEFT, padx=10)

    def validar_numero(self, entry):
        valor = entry.get()
        if valor:
            if not re.match(r'^\d*\.?\d{0,2}$', valor):
                entry.delete(0, tk.END)
                entry.insert(0, valor[:-1])
                messagebox.showwarning("Aviso", "Digite um valor numérico válido (ex: 10.99)")

    def validar_inteiro(self, entry):
        valor = entry.get()
        if valor:
            if not valor.isdigit():
                entry.delete(0, tk.END)
                entry.insert(0, valor[:-1])
                messagebox.showwarning("Aviso", "Digite um número inteiro válido")

    def carregar_fornecedores(self):
        try:
            # Limpa a treeview
            for item in self.tree_fornecedores.get_children():
                self.tree_fornecedores.delete(item)

            fornecedores = self.db.listar_fornecedores()

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
        """Abre a tela de cadastro de fornecedor"""
        TelaCadastroFornecedor(self)
        self.after(500, self.carregar_fornecedores)

    def validar_campos(self):
        """Valida todos os campos do formulário"""
        campos_obrigatorios = [
            (self.entry_nome.get().strip(), "Nome"),
            (self.entry_codigo.get().strip(), "Código"),
            (self.entry_descricao.get().strip(), "Descrição"),
            (self.entry_categoria.get().strip(), "Categoria"),
            (self.entry_preco_custo.get().strip(), "Preço de Custo"),
            (self.entry_preco_venda.get().strip(), "Preço de Venda"),
            (self.entry_estoque_minimo.get().strip(), "Estoque Mínimo")
        ]

        for valor, nome_campo in campos_obrigatorios:
            if not valor:
                raise ValueError(f"O campo {nome_campo} é obrigatório")

        try:
            preco_custo = float(self.entry_preco_custo.get())
            preco_venda = float(self.entry_preco_venda.get())
            estoque_minimo = int(self.entry_estoque_minimo.get())

            if preco_custo < 0 or preco_venda < 0 or estoque_minimo < 0:
                raise ValueError("Valores não podem ser negativos")

            if preco_venda < preco_custo:
                raise ValueError("Preço de venda não pode ser menor que preço de custo")

        except ValueError:
            raise ValueError("Valores numéricos inválidos")


        if not self.fornecedor_selecionado:
            raise ValueError("Selecione um fornecedor para o produto")

        nome_produto = self.entry_nome.get().strip()
        if self.db.verificar_produto_existente(nome_produto, self.fornecedor_selecionado):
            raise ValueError(f"Já existe um produto com o nome '{nome_produto}' para este fornecedor")

    def cadastrar(self):
        try:
            self.validar_campos()

            produto_id = self.db.inserir_produto(
                nome=self.entry_nome.get().strip(),
                codigo=self.entry_codigo.get().strip(),
                descricao=self.entry_descricao.get().strip(),
                categoria=self.entry_categoria.get().strip(),
                fornecedor_id=self.fornecedor_selecionado,
                quantidade=0,  # Inicia com estoque zero
                estoque_minimo=int(self.entry_estoque_minimo.get()),
                preco_custo=float(self.entry_preco_custo.get()),
                preco_venda=float(self.entry_preco_venda.get())
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