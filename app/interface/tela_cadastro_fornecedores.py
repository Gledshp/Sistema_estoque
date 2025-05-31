import tkinter as tk
from tkinter import messagebox
import re
from app.db.db_manager import DBManager


class TelaCadastroFornecedor(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Cadastro de Fornecedor")
        self.geometry("500x400")
        self.db = master.db

        self.criar_widgets()
        self.protocol("WM_DELETE_WINDOW", self.fechar_janela)

    def criar_widgets(self):
        frame_principal = tk.Frame(self)
        frame_principal.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        tk.Label(frame_principal, text="Nome*:").grid(row=0, column=0, sticky="e", pady=5)
        self.entry_nome = tk.Entry(frame_principal, width=40)
        self.entry_nome.grid(row=0, column=1, columnspan=2, sticky="w")

        tk.Label(frame_principal, text="CNPJ:").grid(row=1, column=0, sticky="e", pady=5)
        self.entry_cnpj = tk.Entry(frame_principal, width=25)
        self.entry_cnpj.grid(row=1, column=1, sticky="w")
        self.btn_consultar = tk.Button(frame_principal, text="Consultar CNPJ", command=self.consultar_cnpj)
        self.btn_consultar.grid(row=1, column=2, padx=5)

        # Label para mensagens de erro do CNPJ
        self.label_erro_cnpj = tk.Label(frame_principal, text="", fg="red")
        self.label_erro_cnpj.grid(row=2, column=1, columnspan=2, sticky="w")

        # Contato
        tk.Label(frame_principal, text="Contato:").grid(row=3, column=0, sticky="e", pady=5)
        self.entry_contato = tk.Entry(frame_principal, width=40)
        self.entry_contato.grid(row=3, column=1, columnspan=2, sticky="w")

        # Telefone
        tk.Label(frame_principal, text="Telefone:").grid(row=4, column=0, sticky="e", pady=5)
        self.entry_telefone = tk.Entry(frame_principal, width=40)
        self.entry_telefone.grid(row=4, column=1, columnspan=2, sticky="w")

        # Email
        tk.Label(frame_principal, text="Email:").grid(row=5, column=0, sticky="e", pady=5)
        self.entry_email = tk.Entry(frame_principal, width=40)
        self.entry_email.grid(row=5, column=1, columnspan=2, sticky="w")

        # Endereço
        tk.Label(frame_principal, text="Endereço:").grid(row=6, column=0, sticky="ne", pady=5)
        self.entry_endereco = tk.Text(frame_principal, width=30, height=4)
        self.entry_endereco.grid(row=6, column=1, columnspan=2, sticky="w")

        # Frame para botões
        frame_botoes = tk.Frame(frame_principal)
        frame_botoes.grid(row=10, column=0, columnspan=3, pady=15)

        # Botões
        tk.Button(frame_botoes, text="Cadastrar", command=self.cadastrar).pack(side=tk.RIGHT, padx=5)
        tk.Button(frame_botoes, text="Cancelar", command=self.fechar_janela).pack(side=tk.LEFT, padx=5)

        # Vincular validação do CNPJ enquanto digita
        self.entry_cnpj.bind("<KeyRelease>", self.validar_cnpj_digitacao)

    def formatar_cnpj(self, cnpj):
        return re.sub(r'[^0-9]', '', cnpj)

    def validar_cnpj_digitacao(self, event=None):
        cnpj = self.entry_cnpj.get()
        cnpj_limpo = self.formatar_cnpj(cnpj)

        if not cnpj_limpo:
            self.label_erro_cnpj.config(text="")
            self.btn_consultar.config(state=tk.NORMAL)
            return

        if len(cnpj_limpo) < 14:
            self.label_erro_cnpj.config(text="CNPJ deve ter 14 dígitos")
            self.btn_consultar.config(state=tk.DISABLED)
        elif len(cnpj_limpo) > 14:
            self.label_erro_cnpj.config(text="CNPJ não pode ter mais de 14 dígitos")
            self.btn_consultar.config(state=tk.DISABLED)
        elif not cnpj_limpo.isdigit():
            self.label_erro_cnpj.config(text="CNPJ deve conter apenas números")
            self.btn_consultar.config(state=tk.DISABLED)
        else:
            self.label_erro_cnpj.config(text="")
            self.btn_consultar.config(state=tk.NORMAL)

    def consultar_cnpj(self):
        """Consulta o CNPJ no banco de dados"""
        cnpj = self.formatar_cnpj(self.entry_cnpj.get())

        if len(cnpj) != 14 or not cnpj.isdigit():
            messagebox.showwarning("Atenção", "CNPJ inválido (deve ter exatamente 14 dígitos numéricos)")
            return

        try:
            resultado = self.db.consultar_cnpj(cnpj)

            if resultado['existe']:
                messagebox.showinfo("CNPJ Existente",
                                    f"CNPJ já cadastrado para:\n{resultado['nome']}")
                self.entry_nome.delete(0, tk.END)
                self.entry_nome.insert(0, resultado['nome'])
            else:
                messagebox.showinfo("CNPJ Disponível", "CNPJ não encontrado no sistema")

        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao consultar CNPJ:\n{str(e)}")

    def cadastrar(self):
        try:
            # Validação dos campos
            nome = self.entry_nome.get().strip()
            if not nome:
                raise ValueError("Nome é obrigatório")

            cnpj = self.formatar_cnpj(self.entry_cnpj.get())
            if cnpj and (len(cnpj) != 14 or not cnpj.isdigit()):
                raise ValueError("CNPJ inválido (deve ter 14 dígitos numéricos)")

            # Obter outros campos
            contato = self.entry_contato.get().strip() or None
            telefone = self.entry_telefone.get().strip() or None
            email = self.entry_email.get().strip() or None
            endereco = self.entry_endereco.get("1.0", tk.END).strip() or None

            fornecedor_id = self.db.inserir_fornecedor(
                nome=nome,
                contato=contato,
                telefone=telefone,
                email=email,
                cnpj=cnpj if cnpj else None,
                endereco=endereco
            )

            messagebox.showinfo("Sucesso", f"Fornecedor cadastrado com ID: {fornecedor_id}")
            self.fechar_janela()

        except ValueError as e:
            messagebox.showwarning("Atenção", str(e))
        except Exception as e:
            messagebox.showerror("Erro", f"Falha no cadastro:\n{str(e)}")

    def fechar_janela(self):
        self.destroy()