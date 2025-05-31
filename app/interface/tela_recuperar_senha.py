import tkinter as tk
from tkinter import messagebox
import smtplib
from email.mime.text import MIMEText
import logging


class TelaRecuperarSenha(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Recuperação de Senha")
        self.geometry("400x250")
        self.resizable(False, False)

        self.db = master.db if hasattr(master, 'db') else None
        self._is_destroyed = False

        self.criar_widgets()
        self.protocol("WM_DELETE_WINDOW", self.fechar_janela)

    def criar_widgets(self):
        main_frame = tk.Frame(self, padx=20, pady=20)
        main_frame.pack(expand=True, fill=tk.BOTH)

        tk.Label(main_frame, text="Recuperação de Senha",
                 font=('Arial', 12, 'bold')).pack(pady=(0, 20))

        tk.Label(main_frame, text="Digite seu e-mail cadastrado:").pack(anchor='w')
        self.entry_email = tk.Entry(main_frame, width=40)
        self.entry_email.pack(fill=tk.X, pady=5)

        tk.Button(main_frame, text="Enviar Link de Recuperação",
                  command=self.enviar_email_recuperacao).pack(pady=15)

        tk.Button(main_frame, text="Voltar",
                  command=self.fechar_janela).pack()

    def enviar_email_recuperacao(self):
        email = self.entry_email.get().strip()

        if not email:
            messagebox.showwarning("Atenção", "Digite um e-mail válido")
            return

        try:
            messagebox.showinfo("Sucesso",
                                f"Um link de recuperação foi enviado para {email}\n"
                                "(Simulação - em produção seria enviado de verdade)")

            self.fechar_janela()

        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao enviar e-mail: {str(e)}")
            logging.error(f"Erro ao enviar e-mail de recuperação: {str(e)}")

    def fechar_janela(self):
        self._is_destroyed = True
        self.destroy()

    def __del__(self):
        if not self._is_destroyed:
            self.fechar_janela()