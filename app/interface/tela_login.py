# app/interface/tela_login.py
import tkinter as tk
from tkinter import messagebox
from app.interface.tela_principal import TelaPrincipal
from app.interface.tela_cadastro_usuarios import TelaCadastroUsuarios
from app.db.db_manager import DBManager

class TelaLogin(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Login")
        self.geometry("350x200")
        self.resizable(False, False)

        tk.Label(self, text="Login:").pack(pady=5)
        self.entry_login = tk.Entry(self)
        self.entry_login.pack()

        tk.Label(self, text="Senha:").pack(pady=5)
        self.entry_senha = tk.Entry(self, show="*")
        self.entry_senha.pack()

        tk.Button(self, text="Entrar", command=self.entrar).pack(pady=10)
        tk.Button(self, text="Cadastrar Usuário", command=self.abrir_cadastro).pack()
        tk.Button(self, text="Esqueceu a senha?", command=self.esqueceu_senha).pack(pady=5)

        self.db = DBManager()

    def entrar(self):
        login = self.entry_login.get().strip()
        senha = self.entry_senha.get().strip()

        if not login or not senha:
            messagebox.showwarning("Atenção", "Preencha login e senha")
            return

        if self.db.validar_login(login, senha):
            self.destroy()
            tela_principal = TelaPrincipal()
            tela_principal.mainloop()
        else:
            messagebox.showerror("Erro", "Login ou senha inválidos")

    def abrir_cadastro(self):
        self.withdraw()
        cadastro = TelaCadastroUsuarios(self)
        cadastro.wait_window()
        self.deiconify()

    def esqueceu_senha(self):
        messagebox.showinfo("Esqueceu a senha", "Por favor, entre em contato com o administrador do sistema.")