import tkinter as tk
from tkinter import messagebox, ttk
from app.db.db_manager import DBManager

class TelaCadastroUsuarios(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Cadastro de Usuários")
        self.geometry("350x300")
        self.resizable(False, False)

        self.db = DBManager()

        tk.Label(self, text="Nome:").pack(pady=5)
        self.entry_nome = tk.Entry(self)
        self.entry_nome.pack()

        tk.Label(self, text="Login:").pack(pady=5)
        self.entry_login = tk.Entry(self)
        self.entry_login.pack()

        tk.Label(self, text="Email:").pack(pady=5)
        self.entry_email = tk.Entry(self)
        self.entry_email.pack()

        tk.Label(self, text="Senha:").pack(pady=5)
        self.entry_senha = tk.Entry(self, show="*")
        self.entry_senha.pack()

        tk.Label(self, text="Nível:").pack(pady=5)
        self.combo_nivel = ttk.Combobox(self, values=[1, 2, 3], state="readonly")
        self.combo_nivel.current(0)
        self.combo_nivel.pack()

        tk.Button(self, text="Cadastrar", command=self.cadastrar_usuario).pack(pady=10)

    def cadastrar_usuario(self):
        nome = self.entry_nome.get().strip()
        login = self.entry_login.get().strip()
        email = self.entry_email.get().strip()
        senha = self.entry_senha.get().strip()
        nivel = int(self.combo_nivel.get())

        if not (nome and login and senha):
            messagebox.showwarning("Atenção", "Preencha os campos obrigatórios (Nome, Login, Senha)")
            return

        try:
            self.db.inserir_usuario(nome, login, email, senha, nivel)
            messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso")
            self.destroy()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao cadastrar usuário: {e}")
