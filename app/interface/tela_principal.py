import tkinter as tk
from tkinter import messagebox
from app.interface.tela_cadastro_usuarios import TelaCadastroUsuarios
from app.interface.tela_cadastro_fornecedores import TelaCadastroFornecedores
from app.interface.tela_cadastro_produtos import TelaCadastroProdutos
from app.db.db_manager import DBManager

class TelaPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Estoque - Principal")
        self.geometry("600x400")
        self.resizable(False, False)

        self.db = DBManager()

        btn_usuarios = tk.Button(self, text="Cadastrar Usuário", width=20, command=self.cadastrar_usuario)
        btn_usuarios.pack(pady=10)

        btn_fornecedores = tk.Button(self, text="Cadastrar Fornecedor", width=20, command=self.cadastrar_fornecedor)
        btn_fornecedores.pack(pady=10)

        btn_produtos = tk.Button(self, text="Cadastrar Produto", width=20, command=self.cadastrar_produto)
        btn_produtos.pack(pady=10)

        btn_estoque_baixo = tk.Button(self, text="Ver Estoque Baixo", width=20, command=self.mostrar_estoque_baixo)
        btn_estoque_baixo.pack(pady=10)

        btn_sair = tk.Button(self, text="Sair", width=20, command=self.quit)
        btn_sair.pack(pady=10)

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

    def mostrar_estoque_baixo(self):
        produtos = self.db.produtos_estoque_baixo()
        if not produtos:
            messagebox.showinfo("Estoque Baixo", "Nenhum produto está com estoque baixo.")
        else:
            msg = "Produtos com estoque baixo:\n"
            for nome, qtd, minimo in produtos:
                msg += f"{nome} - Qtde: {qtd}, Mínimo: {minimo}\n"
            messagebox.showwarning("Estoque Baixo", msg)
