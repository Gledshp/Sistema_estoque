import tkinter as tk
from tkinter import messagebox
from app.db.db_manager import DBManager

class TelaCadastroFornecedores(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Cadastro de Fornecedores")
        self.geometry("350x300")
        self.resizable(False, False)

        self.db = DBManager()

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

        tk.Button(self, text="Cadastrar", command=self.cadastrar_fornecedor).pack(pady=10)

    def cadastrar_fornecedor(self):
        nome = self.entry_nome.get().strip()
        contato = self.entry_contato.get().strip()
        telefone = self.entry_telefone.get().strip()
        email = self.entry_email.get().strip()

        if not nome:
            messagebox.showwarning("Atenção", "Nome é obrigatório")
            return

        try:
            self.db.inserir_fornecedor(nome, contato, telefone, email)
            messagebox.showinfo("Sucesso", "Fornecedor cadastrado com sucesso")
            self.destroy()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao cadastrar fornecedor: {e}")
