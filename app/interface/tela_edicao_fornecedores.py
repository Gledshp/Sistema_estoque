import tkinter as tk
from tkinter import messagebox, ttk
from app.db.db_manager import DBManager


class TelaEdicaoFornecedores(tk.Toplevel):
    def __init__(self, master=None, fornecedor_id=None):
        super().__init__(master)
        self.title("Edição de Fornecedor")
        self.geometry("1000x700")
        self.resizable(False, False)

        self.db = master.db if hasattr(master, 'db') else DBManager()
        self.fornecedor_id = fornecedor_id
        self.fornecedor_selecionado = None

        self.criar_widgets()

        if not self.fornecedor_id:
            self.carregar_lista_fornecedores()
        else:
            self.carregar_dados_fornecedor()

    def criar_widgets(self):

        self.frame_lista = tk.Frame(self)
        self.frame_lista.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.frame_edicao = tk.Frame(self)

        self.tree = ttk.Treeview(self.frame_lista, columns=('ID', 'Nome', 'Contato', 'Telefone', 'Email'), show='headings')
        self.tree.heading('ID', text='ID')
        self.tree.heading('Nome', text='Nome')
        self.tree.heading('Contato', text='Contato')
        self.tree.heading('Telefone', text='Telefone')
        self.tree.heading('Email', text='Email')
        self.tree.column('ID', width=50)
        self.tree.column('Nome', width=200)
        self.tree.column('Contato', width=150)
        self.tree.column('Telefone', width=100)
        self.tree.column('Email', width=200)

        scrollbar = ttk.Scrollbar(self.frame_lista, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree.bind('<<TreeviewSelect>>', self.selecionar_fornecedor)

        btn_frame = tk.Frame(self.frame_lista)
        btn_frame.pack(pady=10)

        btn_selecionar = tk.Button(btn_frame, text="Editar Fornecedor", command=self.selecionar_fornecedor)
        btn_selecionar.pack(side=tk.LEFT, padx=5)

        btn_eliminar = tk.Button(btn_frame, text="Eliminar Fornecedor", command=self.eliminar_fornecedor)
        btn_eliminar.pack(side=tk.LEFT, padx=5)

        # Formulário de edição
        tk.Label(self.frame_edicao, text="Nome:").pack(pady=5)
        self.entry_nome = tk.Entry(self.frame_edicao, width=50)
        self.entry_nome.pack()

        tk.Label(self.frame_edicao, text="Contato:").pack(pady=5)
        self.entry_contato = tk.Entry(self.frame_edicao, width=50)
        self.entry_contato.pack()

        tk.Label(self.frame_edicao, text="Telefone:").pack(pady=5)
        self.entry_telefone = tk.Entry(self.frame_edicao, width=50)
        self.entry_telefone.pack()

        tk.Label(self.frame_edicao, text="Email:").pack(pady=5)
        self.entry_email = tk.Entry(self.frame_edicao, width=50)
        self.entry_email.pack()

        tk.Label(self.frame_edicao, text="Endereço:").pack(pady=5)
        self.entry_endereco = tk.Entry(self.frame_edicao, width=50)
        self.entry_endereco.pack()

        btn_edicao_frame = tk.Frame(self.frame_edicao)
        btn_edicao_frame.pack(pady=10)

        btn_salvar = tk.Button(btn_edicao_frame, text="Salvar Alterações", command=self.salvar_alteracoes)
        btn_salvar.pack(side=tk.LEFT, padx=5)

        btn_voltar = tk.Button(btn_edicao_frame, text="Voltar para Lista", command=self.voltar_para_lista)
        btn_voltar.pack(side=tk.LEFT, padx=5)

    def carregar_lista_fornecedores(self):
        fornecedores = self.db.listar_fornecedores()
        self.tree.delete(*self.tree.get_children())

        for fornecedor in fornecedores:
            self.tree.insert('', 'end', values=(
                fornecedor[0],  # ID
                fornecedor[1],  # Nome
                fornecedor[2],  # Contato
                fornecedor[3],  # Telefone
                fornecedor[4]   # Email
            ))

    def selecionar_fornecedor(self, event=None):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Atenção", "Selecione um fornecedor para editar")
            return

        item = self.tree.item(selected_item[0])
        self.fornecedor_id = item['values'][0]

        # Esconde a lista e mostra o formulário de edição
        self.frame_lista.pack_forget()
        self.frame_edicao.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.carregar_dados_fornecedor()

    def voltar_para_lista(self):
        self.frame_edicao.pack_forget()
        self.frame_lista.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.fornecedor_id = None
        self.carregar_lista_fornecedores()

    def carregar_dados_fornecedor(self):
        if not self.fornecedor_id:
            return

        fornecedor = self.db.obter_fornecedor_por_id(self.fornecedor_id)
        if fornecedor:
            self.entry_nome.delete(0, tk.END)
            self.entry_contato.delete(0, tk.END)
            self.entry_telefone.delete(0, tk.END)
            self.entry_email.delete(0, tk.END)
            self.entry_endereco.delete(0, tk.END)

            self.entry_nome.insert(0, fornecedor[1])
            self.entry_contato.insert(0, fornecedor[2])
            self.entry_telefone.insert(0, fornecedor[3])
            self.entry_email.insert(0, fornecedor[4])
            self.entry_endereco.insert(0, fornecedor[5] if len(fornecedor) > 5 else "")

    def salvar_alteracoes(self):
        nome = self.entry_nome.get().strip()
        contato = self.entry_contato.get().strip()
        telefone = self.entry_telefone.get().strip()
        email = self.entry_email.get().strip()
        endereco = self.entry_endereco.get().strip()

        if not nome:
            messagebox.showwarning("Atenção", "Nome é obrigatório")
            return

        try:
            self.db.atualizar_fornecedor(
                self.fornecedor_id, nome, contato, telefone, email, endereco
            )
            messagebox.showinfo("Sucesso", "Fornecedor atualizado com sucesso")
            self.voltar_para_lista()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao atualizar fornecedor: {e}")

    def eliminar_fornecedor(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Atenção", "Selecione um fornecedor para eliminar")
            return

        item = self.tree.item(selected_item[0])
        fornecedor_id = item['values'][0]
        nome = item['values'][1]

        resposta = messagebox.askyesno(
            "Confirmar Eliminação",
            f"Tem certeza que deseja eliminar o fornecedor '{nome}'? Esta ação não pode ser desfeita."
        )

        if resposta:
            try:
                self.db.eliminar_fornecedor(fornecedor_id)
                messagebox.showinfo("Sucesso", "Fornecedor eliminado com sucesso")
                self.carregar_lista_fornecedores()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao eliminar fornecedor: {e}")