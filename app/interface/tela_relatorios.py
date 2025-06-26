import tkinter as tk
from tkinter import ttk, messagebox
import logging


class TelaRelatorios(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Relatório de Estoque")
        self.geometry("1000x600")
        self.db = master.db if hasattr(master, 'db') else DBManager()

        self.criar_widgets()
        self.carregar_dados()
        self.protocol("WM_DELETE_WINDOW", self.fechar_janela)

    def criar_widgets(self):
        main_frame = tk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        filtro_frame = tk.Frame(main_frame)
        filtro_frame.pack(fill=tk.X, pady=(0, 10))

        tk.Label(filtro_frame, text="Filtrar:").pack(side=tk.LEFT, padx=5)
        self.entry_filtro = tk.Entry(filtro_frame, width=40)
        self.entry_filtro.pack(side=tk.LEFT, padx=5)
        self.entry_filtro.bind('<KeyRelease>', self.filtrar_dados)

        btn_filtrar = tk.Button(filtro_frame, text="Filtrar", command=self.filtrar_dados)
        btn_filtrar.pack(side=tk.LEFT, padx=5)

        tree_frame = tk.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        # Treeview para exibir os dados
        self.tree = ttk.Treeview(tree_frame,
                                 columns=("ID", "Nome", "Quantidade", "Mínimo", "Status", "Fornecedor", "Preço Venda"),
                                 show="headings", height=20)

        colunas = [
            ("ID", 50, 'center'),
            ("Nome", 250, 'w'),
            ("Quantidade", 80, 'center'),
            ("Mínimo", 80, 'center'),
            ("Status", 100, 'center'),
            ("Fornecedor", 200, 'w'),
            ("Preço Venda", 100, 'center')
        ]

        for col, width, anchor in colunas:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, anchor=anchor)

        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)

        hsb = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(xscrollcommand=hsb.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        self.tree.tag_configure('ALERTA', background='#ffcccc')  # Vermelho claro para itens com estoque baixo
        self.tree.tag_configure('Normal', background='#ffffff')  # Branco para itens normais

        btn_frame = tk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=10)

        # Botões
        tk.Button(btn_frame, text="Exportar Relatório", command=self.exportar_relatorio).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Atualizar", command=self.carregar_dados).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Fechar", command=self.fechar_janela).pack(side=tk.RIGHT, padx=5)

    def carregar_dados(self, filtro=None):
        try:
            for item in self.tree.get_children():
                self.tree.delete(item)

            produtos = self.db.listar_produtos_relatorio(filtro)

            if not produtos:
                messagebox.showinfo("Informação", "Nenhum produto encontrado com os critérios selecionados.")
                return

            for produto in produtos:
                status = "ALERTA" if produto[2] < produto[3] else "Normal"
                preco_venda = f"R$ {produto[6]:.2f}" if produto[6] else "N/A"

                self.tree.insert("", tk.END, values=(
                    produto[0],  # ID
                    produto[1],  # Nome
                    produto[2],  # Quantidade
                    produto[3],  # Estoque mínimo
                    status,  # Status
                    produto[5],  # Fornecedor
                    preco_venda  # Preço de venda
                ), tags=(status,))

        except Exception as e:
            logging.error(f"Erro ao carregar estoque: {str(e)}", exc_info=True)
            messagebox.showerror("Erro", f"Falha ao carregar dados: {str(e)}")

    def filtrar_dados(self, event=None):
        filtro = self.entry_filtro.get().strip()
        self.carregar_dados(filtro if filtro else None)

    def exportar_relatorio(self):
        try:
            from datetime import datetime
            import os

            relatorios_dir = os.path.join(os.path.dirname(__file__), "..", "relatorios")
            os.makedirs(relatorios_dir, exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            arquivo = os.path.join(relatorios_dir, f"relatorio_estoque_{timestamp}.txt")

            with open(arquivo, 'w', encoding='utf-8') as f:
                f.write("Relatório de Estoque\n")
                f.write(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n")
                f.write("ID | Nome | Quantidade | Mínimo | Status | Fornecedor | Preço Venda\n")
                f.write("-" * 100 + "\n")

                for item in self.tree.get_children():
                    valores = self.tree.item(item, 'values')
                    linha = " | ".join(str(v) for v in valores)
                    f.write(linha + "\n")

            messagebox.showinfo("Sucesso", f"Relatório exportado com sucesso para:\n{arquivo}")
        except Exception as e:
            logging.error(f"Erro ao exportar relatório: {str(e)}", exc_info=True)
            messagebox.showerror("Erro", f"Falha ao exportar relatório: {str(e)}")

    def fechar_janela(self):
        try:
            if hasattr(self, 'db') and self.db != getattr(self.master, 'db', None):
                self.db.fechar()
            self.destroy()
        except Exception as e:
            logging.error(f"Erro ao fechar janela: {str(e)}")
            self.destroy()