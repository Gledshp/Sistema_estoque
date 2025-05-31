import tkinter as tk
from tkinter import messagebox, ttk
from app.db.db_manager import DBManager
import logging


class TelaMovimentacaoEstoque(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Movimentação de Estoque")
        self.geometry("500x350")
        self.db = master.db if hasattr(master, 'db') else DBManager()

        self.criar_widgets()
        self.carregar_produtos()
        self.protocol("WM_DELETE_WINDOW", self.fechar_janela)
        self.center_window()

    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def criar_widgets(self):
        main_frame = tk.Frame(self, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(main_frame, text="Produto*:").pack(anchor='w', pady=(0, 5))
        self.combo_produto = ttk.Combobox(main_frame, state="readonly")
        self.combo_produto.pack(fill=tk.X, pady=(0, 10))

        tk.Label(main_frame, text="Tipo*:").pack(anchor='w', pady=(0, 5))
        self.combo_tipo = ttk.Combobox(
            main_frame,
            values=["Entrada (Adicionar ao estoque)", "Saída (Remover do estoque)"],
            state="readonly"
        )
        self.combo_tipo.current(0)
        self.combo_tipo.pack(fill=tk.X, pady=(0, 10))

        tk.Label(main_frame, text="Quantidade*:").pack(anchor='w', pady=(0, 5))
        self.entry_quantidade = tk.Entry(main_frame)
        self.entry_quantidade.pack(fill=tk.X, pady=(0, 15))

        btn_frame = tk.Frame(main_frame)
        btn_frame.pack(pady=10)

        tk.Button(
            btn_frame,
            text="Registrar",
            command=self.registrar_movimentacao,
            width=15
        ).pack(side=tk.LEFT, padx=10)

        tk.Button(
            btn_frame,
            text="Cancelar",
            command=self.fechar_janela,
            width=15
        ).pack(side=tk.RIGHT, padx=10)

    def carregar_produtos(self):
        try:
            produtos = self.db.listar_produtos()
            self.produtos_ids = [p[0] for p in produtos]
            nomes = [f"{p[2]} - {p[1]} (Estoque: {p[3]})" for p in produtos]
            self.combo_produto['values'] = nomes

            if nomes:
                self.combo_produto.current(0)
            else:
                messagebox.showwarning(
                    "Atenção",
                    "Nenhum produto cadastrado. Cadastre produtos primeiro."
                )
                self.fechar_janela()

        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao carregar produtos: {str(e)}")
            logging.error(f"Erro ao carregar produtos: {str(e)}", exc_info=True)
            self.fechar_janela()

    def registrar_movimentacao(self):
        try:
            produto_idx = self.combo_produto.current()
            if produto_idx == -1:
                raise ValueError("Selecione um produto")

            tipo = "entrada" if self.combo_tipo.current() == 0 else "saida"

            try:
                quantidade = int(self.entry_quantidade.get())
                if quantidade <= 0:
                    raise ValueError("Quantidade deve ser maior que zero")
            except ValueError:
                raise ValueError("Informe uma quantidade válida")

            produto_id = self.produtos_ids[produto_idx]

            usuario_data = getattr(self.master, 'usuario', None)
            if not usuario_data or not hasattr(usuario_data, 'get') or not usuario_data.get('id'):
                raise ValueError("Usuário não autenticado ou dados incompletos")

            usuario_id = usuario_data['id']

            self.db.registrar_movimentacao(
                produto_id=produto_id,
                tipo=tipo,
                quantidade=quantidade,
                usuario_id=usuario_id
            )

            messagebox.showinfo(
                "Sucesso",
                f"Movimentação registrada com sucesso!\n\n"
                f"Produto ID: {produto_id}\n"
                f"Tipo: {'Entrada' if tipo == 'entrada' else 'Saída'}\n"
                f"Quantidade: {quantidade}"
            )
            self.fechar_janela()

        except ValueError as e:
            messagebox.showwarning("Atenção", str(e))
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao registrar movimentação: {str(e)}")
            logging.error(f"Erro ao registrar movimentação: {str(e)}", exc_info=True)

    def fechar_janela(self):
        try:
            if hasattr(self, 'db') and self.db != getattr(self.master, 'db', None):
                self.db.fechar()
            self.destroy()
        except Exception as e:
            logging.error(f"Erro ao fechar janela: {str(e)}")
            self.destroy()