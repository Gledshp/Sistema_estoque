import tkinter as tk
from tkinter import messagebox
from app.db.db_manager import DBManager


class TelaEdicaoFornecedores(tk.Toplevel):
    def __init__(self, master=None, fornecedor_id=None):
        super().__init__(master)
        self.title("Edição de Fornecedor")
        self.geometry("350x300")
        self.resizable(False, False)

        self.db = DBManager()
        self.fornecedor_id = fornecedor_id

        self.criar_widgets()
        self.carregar_dados_fornecedor()

    def criar_widgets(self):
        tk.Label(self, text="Nome:").pack(pady=5)
        self.entry_nome = tk.Entry(self)
        self.entry_nome.pack()

        tk.Label(self, text="Contato:").pack(pady=5)
        self.entry_contato = tk.Entry(self)
        self.entry_contato.pack()

        tk.Label(self, text="Telefone:").pack(pady=5)
        self.entry_telefone = tk.Entry(self)
        self.entry_telefone.pack()

        tk.Label(self, text="Email:").pack(pady=5)
        self.entry_email = tk.Entry(self)
        self.entry_email.pack()

        btn_salvar = tk.Button(self, text="Salvar Alterações", command=self.salvar_alteracoes)
        btn_salvar.pack(pady=10)

    def carregar_dados_fornecedor(self):
        if not self.fornecedor_id:
            return

        fornecedor = self.db.obter_fornecedor_por_id(self.fornecedor_id)
        if fornecedor:
            self.entry_nome.insert(0, fornecedor[1])
            self.entry_contato.insert(0, fornecedor[2])
            self.entry_telefone.insert(0, fornecedor[3])
            self.entry_email.insert(0, fornecedor[4])

    def salvar_alteracoes(self):
        nome = self.entry_nome.get().strip()
        contato = self.entry_contato.get().strip()
        telefone = self.entry_telefone.get().strip()
        email = self.entry_email.get().strip()

        if not nome:
            messagebox.showwarning("Atenção", "Nome é obrigatório")
            return

        try:
            self.db.atualizar_fornecedor(
                self.fornecedor_id, nome, contato, telefone, email
            )
            messagebox.showinfo("Sucesso", "Fornecedor atualizado com sucesso")
            self.destroy()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao atualizar fornecedor: {e}")