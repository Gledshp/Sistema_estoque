import tkinter as tk
from tkinter import messagebox, ttk
from app.db.db_manager import DBManager
import logging


class TelaEdicaoProdutos(tk.Toplevel):
    def __init__(self, master=None, produto_id=None):
        super().__init__(master)
        self.title("Edição de Produto")
        self.geometry("1000x700")
        self.resizable(False, False)

        self.db = master.db if hasattr(master, 'db') else DBManager()
        self.produto_id = produto_id
        self.produto_selecionado = None
        self.fornecedores_dict = {}

        self.criar_widgets()

        if not self.produto_id:
            self.carregar_lista_produtos()
        else:
            self.carregar_dados_produto()

    def criar_widgets(self):

        self.frame_lista = tk.Frame(self)
        self.frame_lista.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.frame_edicao = tk.Frame(self)

        # Lista de produtos
        self.tree = ttk.Treeview(self.frame_lista, columns=('ID', 'Nome', 'Código', 'Quantidade', 'Preço'),
                                 show='headings')
        self.tree.heading('ID', text='ID')
        self.tree.heading('Nome', text='Nome')
        self.tree.heading('Código', text='Código')
        self.tree.heading('Quantidade', text='Quantidade')
        self.tree.heading('Preço', text='Preço Venda')
        self.tree.column('ID', width=50)
        self.tree.column('Nome', width=200)
        self.tree.column('Código', width=100)
        self.tree.column('Quantidade', width=80)
        self.tree.column('Preço', width=100)

        scrollbar = ttk.Scrollbar(self.frame_lista, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree.bind('<<TreeviewSelect>>', self.on_produto_selecionado)

        btn_frame_lista = tk.Frame(self.frame_lista)
        btn_frame_lista.pack(pady=10)

        btn_selecionar = tk.Button(btn_frame_lista, text="Editar Produto", command=self.editar_produto_selecionado)
        btn_selecionar.pack(side=tk.LEFT, padx=5)

        btn_eliminar = tk.Button(btn_frame_lista, text="Eliminar Produto", command=self.eliminar_produto)
        btn_eliminar.pack(side=tk.LEFT, padx=5)

        tk.Label(self.frame_edicao, text="Nome:").pack(pady=5)
        self.entry_nome = tk.Entry(self.frame_edicao, width=50)
        self.entry_nome.pack()

        tk.Label(self.frame_edicao, text="Código:").pack(pady=5)
        self.entry_codigo = tk.Entry(self.frame_edicao, width=50)
        self.entry_codigo.pack()

        tk.Label(self.frame_edicao, text="Descrição:").pack(pady=5)
        self.entry_descricao = tk.Entry(self.frame_edicao, width=50)
        self.entry_descricao.pack()

        tk.Label(self.frame_edicao, text="Categoria:").pack(pady=5)
        self.entry_categoria = tk.Entry(self.frame_edicao, width=50)
        self.entry_categoria.pack()

        tk.Label(self.frame_edicao, text="Fornecedor:").pack(pady=5)
        self.combo_fornecedor = ttk.Combobox(self.frame_edicao, state="readonly", width=47)
        self.combo_fornecedor.pack()
        self.atualizar_fornecedores()

        tk.Label(self.frame_edicao, text="Quantidade em estoque:").pack(pady=5)
        self.entry_quantidade = tk.Entry(self.frame_edicao, width=50)
        self.entry_quantidade.pack()

        tk.Label(self.frame_edicao, text="Estoque mínimo:").pack(pady=5)
        self.entry_estoque_minimo = tk.Entry(self.frame_edicao, width=50)
        self.entry_estoque_minimo.pack()

        tk.Label(self.frame_edicao, text="Preço de custo:").pack(pady=5)
        self.entry_preco_custo = tk.Entry(self.frame_edicao, width=50)
        self.entry_preco_custo.pack()

        tk.Label(self.frame_edicao, text="Preço de venda:").pack(pady=5)
        self.entry_preco_venda = tk.Entry(self.frame_edicao, width=50)
        self.entry_preco_venda.pack()

        btn_frame_edicao = tk.Frame(self.frame_edicao)
        btn_frame_edicao.pack(pady=10)

        btn_salvar = tk.Button(btn_frame_edicao, text="Salvar Alterações", command=self.salvar_alteracoes)
        btn_salvar.pack(side=tk.LEFT, padx=5)

        btn_voltar = tk.Button(btn_frame_edicao, text="Voltar para Lista", command=self.voltar_para_lista)
        btn_voltar.pack(side=tk.LEFT, padx=5)

    def carregar_lista_produtos(self):
        try:
            produtos = self.db.listar_produtos()
            self.tree.delete(*self.tree.get_children())

            for produto in produtos:
                self.tree.insert('', 'end', values=(
                    produto[0],  # ID
                    produto[1],  # Nome
                    produto[2],  # Código
                    produto[3],  # Quantidade
                    f"R$ {produto[4]:.2f}" if produto[4] else "R$ 0.00"  # Preço de venda
                ))
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar produtos: {e}")

    def on_produto_selecionado(self, event):
        """Método chamado quando um item é selecionado na Treeview"""
        selected_item = self.tree.selection()
        if selected_item:
            item = self.tree.item(selected_item[0])
            self.produto_id = item['values'][0]

    def editar_produto_selecionado(self):
        """Método chamado quando o botão Editar é clicado"""
        if not self.produto_id:
            messagebox.showwarning("Atenção", "Selecione um produto para editar")
            return

        self.frame_lista.pack_forget()
        self.frame_edicao.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.carregar_dados_produto()

    def eliminar_produto(self):
        if not self.produto_id:
            messagebox.showwarning("Atenção", "Selecione um produto para eliminar")
            return

        selected_item = self.tree.selection()
        if not selected_item:
            return

        item = self.tree.item(selected_item[0])
        produto_id = item['values'][0]
        nome = item['values'][1]

        resposta = messagebox.askyesno(
            "Confirmar Eliminação",
            f"Tem certeza que deseja eliminar o produto '{nome}'? Esta ação não pode ser desfeita."
        )

        if resposta:
            try:
                self.db.eliminar_produto(produto_id)
                messagebox.showinfo("Sucesso", "Produto eliminado com sucesso")
                self.carregar_lista_produtos()
                self.produto_id = None  # Resetar o ID após eliminação
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao eliminar produto: {e}")

    def voltar_para_lista(self):
        self.frame_edicao.pack_forget()
        self.frame_lista.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.produto_id = None
        self.carregar_lista_produtos()

    def atualizar_fornecedores(self):
        try:
            fornecedores = self.db.listar_fornecedores()
            self.fornecedores_dict = {f[1]: f[0] for f in fornecedores}  # nome: id
            nomes = list(self.fornecedores_dict.keys())
            self.combo_fornecedor['values'] = nomes
            if nomes:
                self.combo_fornecedor.current(0)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar fornecedores: {e}")

    def carregar_dados_produto(self):
        if not self.produto_id:
            return

        try:
            produto = self.db.obter_produto_por_id(self.produto_id)
            if not produto:
                messagebox.showerror("Erro", "Produto não encontrado")
                self.voltar_para_lista()
                return

            self.entry_nome.delete(0, tk.END)
            self.entry_codigo.delete(0, tk.END)
            self.entry_descricao.delete(0, tk.END)
            self.entry_categoria.delete(0, tk.END)
            self.entry_quantidade.delete(0, tk.END)
            self.entry_estoque_minimo.delete(0, tk.END)
            self.entry_preco_custo.delete(0, tk.END)
            self.entry_preco_venda.delete(0, tk.END)

            self.entry_nome.insert(0, produto[1] or "")
            self.entry_codigo.insert(0, produto[2] or "")
            self.entry_descricao.insert(0, produto[3] or "")
            self.entry_categoria.insert(0, produto[4] or "")

            fornecedor_id = produto[5]
            if fornecedor_id:
                fornecedor = self.db.obter_fornecedor_por_id(fornecedor_id)
                if fornecedor:
                    self.combo_fornecedor.set(fornecedor[1])

            self.entry_quantidade.insert(0, str(produto[6]) if produto[6] is not None else "0")
            self.entry_estoque_minimo.insert(0, str(produto[7]) if produto[7] is not None else "0")
            self.entry_preco_custo.insert(0, f"{produto[8]:.2f}" if produto[8] is not None else "0.00")
            self.entry_preco_venda.insert(0, f"{produto[9]:.2f}" if produto[9] is not None else "0.00")

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar dados do produto: {e}")
            self.voltar_para_lista()

    def salvar_alteracoes(self):
        # Obter valores dos campos
        nome = self.entry_nome.get().strip()
        codigo = self.entry_codigo.get().strip()
        descricao = self.entry_descricao.get().strip()
        categoria = self.entry_categoria.get().strip()
        fornecedor_nome = self.combo_fornecedor.get()
        quantidade_str = self.entry_quantidade.get().strip()
        estoque_minimo_str = self.entry_estoque_minimo.get().strip()
        preco_custo_str = self.entry_preco_custo.get().strip()
        preco_venda_str = self.entry_preco_venda.get().strip()

        # Validações
        if not nome:
            messagebox.showwarning("Atenção", "Nome do produto é obrigatório")
            return

        try:
            quantidade = int(quantidade_str) if quantidade_str else 0
            estoque_minimo = int(estoque_minimo_str) if estoque_minimo_str else 0
            preco_custo = float(preco_custo_str) if preco_custo_str else 0.0
            preco_venda = float(preco_venda_str) if preco_venda_str else 0.0

            if quantidade < 0 or estoque_minimo < 0 or preco_custo < 0 or preco_venda < 0:
                raise ValueError("Valores não podem ser negativos")

        except ValueError as e:
            messagebox.showwarning("Atenção", f"Valores inválidos: {e}\n\n"
                                              "Quantidades devem ser números inteiros\n"
                                              "Preços devem ser números decimais\n"
                                              "Todos os valores devem ser positivos")
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
            self.voltar_para_lista()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao atualizar produto: {e}")