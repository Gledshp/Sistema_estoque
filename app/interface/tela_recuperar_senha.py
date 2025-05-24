import tkinter as tk
from tkinter import messagebox

class TelaRecuperarSenha(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Recuperar Senha")
        self.geometry("300x150")

        tk.Label(self, text="Funcionalidade não implementada ainda.").pack(pady=30)
        tk.Button(self, text="Fechar", command=self.destroy).pack()
