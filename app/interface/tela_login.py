import tkinter as tk
from tkinter import messagebox
import logging
from app.db.db_manager import DBManager
from app.interface.tela_principal import TelaPrincipal
from app.interface.tela_cadastro_usuarios import TelaCadastroUsuarios
from app.interface.tela_recuperar_senha import TelaRecuperarSenha


class TelaLogin(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Login - Sistema de Estoque")
        self.geometry("400x300")
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.fechar_aplicacao)

        self.db = None
        self.inicializar_banco_dados()
        self.criar_widgets()
        self.center_window()
        self.entry_login.focus_set()

    def inicializar_banco_dados(self):
        try:
            self.db = DBManager()
            logging.info("Banco de dados inicializado com sucesso")
        except Exception as e:
            logging.error(f"Falha ao conectar ao banco: {str(e)}")
            messagebox.showerror("Erro Crítico", f"Falha ao conectar ao banco de dados:\n{str(e)}")
            self.destroy()

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

        tk.Label(main_frame, text="Login", font=('Arial', 14, 'bold')).pack(pady=(0, 20))

        entry_frame = tk.Frame(main_frame)
        entry_frame.pack(fill=tk.X, pady=5)

        tk.Label(entry_frame, text="Usuário:").pack(anchor='w')
        self.entry_login = tk.Entry(entry_frame)
        self.entry_login.pack(fill=tk.X, pady=5)
        self.entry_login.bind('<Return>', lambda e: self.entry_senha.focus_set())

        tk.Label(entry_frame, text="Senha:").pack(anchor='w')
        self.entry_senha = tk.Entry(entry_frame, show="*")
        self.entry_senha.pack(fill=tk.X, pady=5)
        self.entry_senha.bind('<Return>', lambda e: self.entrar())

        btn_frame = tk.Frame(main_frame)
        btn_frame.pack(pady=15)

        self.btn_entrar = tk.Button(btn_frame, text="Entrar", command=self.entrar, width=10)
        self.btn_entrar.pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Sair", command=self.fechar_aplicacao, width=10).pack(side=tk.LEFT, padx=5)

        links_frame = tk.Frame(main_frame)
        links_frame.pack(pady=10)

        self.lbl_cadastro = tk.Label(links_frame, text="Novo usuário?", fg="blue", cursor="hand2")
        self.lbl_cadastro.pack(side=tk.LEFT)
        tk.Label(links_frame, text=" | ").pack(side=tk.LEFT)
        self.lbl_recuperar = tk.Label(links_frame, text="Esqueceu a senha?", fg="blue", cursor="hand2")
        self.lbl_recuperar.pack(side=tk.LEFT)

        self.lbl_cadastro.bind("<Button-1>", lambda e: self.abrir_cadastro())
        self.lbl_recuperar.bind("<Button-1>", lambda e: self.abrir_recuperacao_senha())

    def abrir_cadastro(self):
        self.withdraw()
        TelaCadastroUsuarios(self, modo_cadastro=True)

    def abrir_recuperacao_senha(self):
        self.withdraw()
        TelaRecuperarSenha(self)

    def entrar(self):
        login = self.entry_login.get().strip()
        senha = self.entry_senha.get().strip()

        if not login or not senha:
            messagebox.showwarning("Atenção", "Preencha todos os campos")
            self.entry_login.focus_set()
            return

        try:
            self.btn_entrar.config(state=tk.DISABLED)
            self.update()

            usuario = self.db.validar_login(login, senha)
            if usuario:
                self.withdraw()
                TelaPrincipal(self, usuario)
            else:
                messagebox.showerror("Erro", "Credenciais inválidas")
                self.entry_senha.delete(0, tk.END)
                self.entry_login.focus_set()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha no login: {str(e)}")
            logging.error(f"Erro no login: {str(e)}")
        finally:
            self.btn_entrar.config(state=tk.NORMAL)

    def fechar_aplicacao(self):
        try:
            if hasattr(self, 'db') and self.db:
                self.db.fechar()
            self.destroy()
        except Exception as e:
            logging.error(f"Erro ao fechar aplicação: {str(e)}")
            self.destroy()

    def show(self):
        self.update()
        self.deiconify()
        self.center_window()
        self.entry_login.focus_set()