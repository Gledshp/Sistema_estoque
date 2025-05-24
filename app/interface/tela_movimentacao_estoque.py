import tkinter as tk
from tkinter import messagebox, ttk
from app.db.db_manager import DBManager

class TelaMovimentacaoEstoque(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Movimentação de Estoque")
        self.geometry("400x300")
        self.db = DBManager()

        tk.Label(self, text="Produto:").pack(pady=5)
        self.combo_produto = ttk.Combobox(self, state="readonly")
        self.combo_produto.pack()
        self.atualizar_produtos()

        tk.Label(self, text="Tipo:").pack(pady=5)
        self.combo_tipo = ttk.Combobox(self, values=["entrada", "saida"], state="readonly")
        self.combo_tipo.current(0)
        self.combo_tipo.pack()

        tk.Label(self, text="Quantidade:").pack(pady=5)
        self.entry_quantidade = tk.Entry(self)
        self.entry_quantidade.pack()

        tk.Button(self, text="Registrar Movimentação", command=self.registrar_movimentacao).pack(pady=10)

    def atualizar_produtos(self):
        produtos = self.db.listar_produtos()
        self.produtos_ids = [p[0] for p in produtos]
        nomes = [f"{p[2]} - {p[1]}" for p in produtos]  # código - nome
        self.combo_produto['values'] = nomes
        if nomes:
            self.combo_produto.current(0)

    def registrar_movimentacao(self):
        idx = self.combo_produto.current()
        if idx == -1:
            messagebox.showwarning("Atenção", "Selecione um produto")
            return

        tipo = self.combo_tipo.get()
        try:
            quantidade = int(self.entry_quantidade.get())
            if quantidade <= 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Atenção", "Informe uma quantidade válida")
            return

        produto_id = self.produtos_ids[idx]

        try:
            self.db.registrar_movimentacao(produto_id, tipo, quantidade)
            messagebox.showinfo("Sucesso", "Movimentação registrada")
            self.destroy()
        except Exception as e:
            messagebox.showerror("Erro", str(e))
