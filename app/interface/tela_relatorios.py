import tkinter as tk
from tkinter import ttk
from app.db.db_manager import DBManager
import logging


class TelaRelatorios(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Relatório de Estoque")
        self.geometry("800x600")
        self.db = master.db if hasattr(master, 'db') else DBManager()

        self.criar_widgets()
        self.protocol("WM_DELETE_WINDOW", self.fechar_janela)
        self.carregar_dados()

    def criar_widgets(self):
        self.tree = ttk.Treeview(self, columns=("ID", "Nome", "Quantidade", "Mínimo", "Status"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("Quantidade", text="Quantidade")
        self.tree.heading("Mínimo", text="Estoque Mínimo")
        self.tree.heading("Status", text="Status")

        self.tree.column("ID", width=50)
        self.tree.column("Nome", width=200)
        self.tree.column("Quantidade", width=80)
        self.tree.column("Mínimo", width=80)
        self.tree.column("Status", width=100)

        scroll = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

    def carregar_dados(self):
        try:
            produtos = self.db.listar_produtos()

            for produto in produtos:
                status = "Normal"
                if produto[6] < produto[7]:
                    status = "ALERTA"

                self.tree.insert("", "end", values=(
                    produto[0],
                    produto[1],
                    produto[6],
                    produto[7],
                    status
                ))

        except Exception as e:
            logging.error(f"Erro ao carregar estoque: {str(e)}", exc_info=True)
            tk.messagebox.showerror("Erro", f"Falha ao carregar dados: {str(e)}")

    def fechar_janela(self):
        try:
            self.destroy()
        except Exception as e:
            logging.error(f"Erro ao fechar janela: {str(e)}")
            self.destroy()