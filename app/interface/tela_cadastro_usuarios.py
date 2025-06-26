import tkinter as tk
from tkinter import ttk, messagebox
from hashlib import sha256
from app.db.db_manager import DBManager
import logging


class TelaCadastroUsuarios(tk.Toplevel):
    def __init__(self, master=None, modo_cadastro=False):
        super().__init__(master)
        self._is_destroyed = False
        self.title("Cadastro de Usuários")
        self.geometry("400x450")
        self.resizable(False, False)
        self.modo_cadastro = modo_cadastro
        self.master = master

        try:
            self.db = master.db if hasattr(master, 'db') else DBManager()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao conectar ao banco: {str(e)}")
            self.destroy()
            return

        self.criar_widgets()
        self.center_window()
        self.protocol("WM_DELETE_WINDOW", self.fechar_janela)

    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def criar_widgets(self):
        main_frame = tk.Frame(self, padx=20, pady=20)
        main_frame.pack(expand=True, fill=tk.BOTH)

        tk.Label(main_frame, text="Cadastro de Usuário",
                 font=('Arial', 14, 'bold')).pack(pady=(0, 20))

        campos = [
            ("Nome*:", tk.Entry(main_frame)),
            ("Login*:", tk.Entry(main_frame)),
            ("E-mail:", tk.Entry(main_frame)),
            ("Senha*:", tk.Entry(main_frame, show="*")),
            ("Confirmar Senha*:", tk.Entry(main_frame, show="*")),
            ("Nível*:", ttk.Combobox(main_frame, values=[1, 2, 3], state="readonly"))
        ]

        self.entries = {}
        for i, (label_text, widget) in enumerate(campos):
            tk.Label(main_frame, text=label_text, anchor='w').pack(fill=tk.X)
            widget.pack(fill=tk.X, pady=5)
            self.entries[label_text.replace(':', '').replace('*', '').strip().lower()] = widget

        self.entries['nível'].current(0)

        tk.Button(main_frame, text="Cadastrar", command=self.cadastrar_usuario,
                  bg="#4CAF50", fg="white", height=2).pack(fill=tk.X, pady=10)

    def cadastrar_usuario(self):
        nome = self.entries['nome'].get().strip()
        login = self.entries['login'].get().strip()
        email = self.entries['e-mail'].get().strip()
        senha = self.entries['senha'].get().strip()
        confirmar_senha = self.entries['confirmar senha'].get().strip()
        nivel = int(self.entries['nível'].get())

        if not (nome and login and senha):
            messagebox.showwarning("Atenção", "Preencha os campos obrigatórios (*)")
            return

        if senha != confirmar_senha:
            messagebox.showwarning("Atenção", "As senhas não coincidem")
            return

        try:
            senha_hash = sha256(senha.encode()).hexdigest()
            self.db.inserir_usuario(nome, login, email, senha_hash, nivel)
            messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso")
            self.fechar_janela()
        except ValueError as e:
            messagebox.showwarning("Atenção", str(e))
        except Exception as e:
            messagebox.showerror("Erro", f"Falha no cadastro: {str(e)}")

    def fechar_janela(self):
        self._is_destroyed = True
        if self.master:
            self.master.deiconify()
        self.destroy()

    def __del__(self):
        if hasattr(self, '_is_destroyed') and not self._is_destroyed:
            self.fechar_janela()