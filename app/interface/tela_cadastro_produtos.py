import tkinter as tk
from tkinter import messagebox, ttk
from app.db.db_manager import DBManager
from app.interface.tela_cadastro_fornecedores import TelaCadastroFornecedores


class TelaCadastroProdutos(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Cadastro de Produtos")
        self.geometry("500x600")  # Tamanho ajustado para todos os campos
        self.resizable(False, False)

        # Conexão com o banco de dados
        self.db = DBManager()

        # Frame principal
        main_frame = tk.Frame(self, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Campos do formulário (organizados em grid)
        row = 0
        campos = [
            ("Nome*:", "entry_nome"),
            ("Código:", "entry_codigo"),
            ("Descrição:", "entry_descricao"),
            ("Categoria:", "entry_categoria"),
            ("Fornecedor:", "combo_fornecedor"),
            ("Quantidade:", "entry_quantidade"),
            ("Estoque mínimo:", "entry_estoque_minimo"),
            ("Preço de custo:", "entry_preco_custo"),
            ("Preço de venda:", "entry_preco_venda")
        ]

        for label_text, attr_name in campos:
            tk.Label(main_frame, text=label_text).grid(row=row, column=0, sticky="w", pady=5)

            if "combo" in attr_name:
                entry = ttk.Combobox(main_frame, state="readonly", width=40)
                setattr(self, attr_name, entry)
                self.atualizar_fornecedores()
            else:
                entry = tk.Entry(main_frame, width=43)
                setattr(self, attr_name, entry)

                # Valores padrão para campos numéricos
                if "quantidade" in attr_name or "estoque_minimo" in attr_name:
                    entry.insert(0, "0")
                elif "preco" in attr_name:
                    entry.insert(0, "0.0")

            entry.grid(row=row, column=1, sticky="ew", padx=5, pady=5)
            row += 1

        # Frame para botões
        buttons_frame = tk.Frame(main_frame)
        buttons_frame.grid(row=row, column=0, columnspan=2, pady=20)

        tk.Button(
            buttons_frame,
            text="Cadastrar Produto",
            command=self.cadastrar_produto
        ).pack(side=tk.LEFT, padx=10)

        tk.Button(
            buttons_frame,
            text="Cadastrar Fornecedor",
            command=self.cadastrar_fornecedor
        ).pack(side=tk.LEFT, padx=10)

        tk.Button(
            buttons_frame,
            text="Cancelar",
            command=self.destroy
        ).pack(side=tk.RIGHT, padx=10)

    def atualizar_fornecedores(self):
        fornecedores = self.db.listar_fornecedores()
        nomes = [f[1] for f in fornecedores]  # Pega o nome do fornecedor (índice 1)
        self.combo_fornecedor['values'] = nomes
        if nomes:
            self.combo_fornecedor.current(0)

    def cadastrar_produto(self):
        dados = {
            'nome': self.entry_nome.get().strip(),
            'codigo': self.entry_codigo.get().strip(),
            'descricao': self.entry_descricao.get().strip(),
            'categoria': self.entry_categoria.get().strip(),
            'fornecedor_nome': self.combo_fornecedor.get(),
            'quantidade': self.entry_quantidade.get().strip(),
            'estoque_minimo': self.entry_estoque_minimo.get().strip(),
            'preco_custo': self.entry_preco_custo.get().strip(),
            'preco_venda': self.entry_preco_venda.get().strip()
        }

        if not dados['nome']:
            messagebox.showwarning("Atenção", "Nome do produto é obrigatório")
            return
        try:
            dados['quantidade'] = int(dados['quantidade']) if dados['quantidade'] else 0
            dados['estoque_minimo'] = int(dados['estoque_minimo']) if dados['estoque_minimo'] else 0
            dados['preco_custo'] = float(dados['preco_custo']) if dados['preco_custo'] else 0.0
            dados['preco_venda'] = float(dados['preco_venda']) if dados['preco_venda'] else 0.0
        except ValueError:
            messagebox.showwarning("Atenção", "Quantidades e preços devem ser numéricos")
            return
        fornecedor_id = None
        if dados['fornecedor_nome']:
            fornecedores = self.db.listar_fornecedores()
            for f in fornecedores:
                if f[1] == dados['fornecedor_nome']:
                    fornecedor_id = f[0]
                    break
        try:
            self.db.inserir_produto(
                dados['nome'], dados['codigo'], dados['descricao'], dados['categoria'], fornecedor_id,
                dados['quantidade'], dados['estoque_minimo'], dados['preco_custo'], dados['preco_venda']
            )
            messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso")
            self.destroy()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao cadastrar produto: {str(e)}")

    def cadastrar_fornecedor(self):
        self.withdraw()  # Esconde a janela atual
        TelaCadastroFornecedores(self).wait_window()  # Abre a tela de fornecedores
        self.atualizar_fornecedores()  # Atualiza a lista ao retornar
        self.deiconify()  # Mostra a janela novamente