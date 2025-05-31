import tkinter as tk
from tkinter import ttk, messagebox
from app.db.db_manager import DBManager
from app.interface.tela_cadastro_produtos import TelaCadastroProduto
from app.interface.tela_cadastro_fornecedores import TelaCadastroFornecedor
from app.interface.tela_cadastro_usuarios import TelaCadastroUsuarios
from app.interface.tela_cotacao_moedas import TelaCotacaoMoedas
from app.interface.tela_relatorios import TelaRelatorios
from app.interface.tela_edicao_produtos import TelaEdicaoProdutos
from app.interface.tela_edicao_fornecedores import TelaEdicaoFornecedores
from app.interface.tela_movimentacao_estoque import TelaMovimentacaoEstoque


class TelaPrincipal(tk.Toplevel):
    def __init__(self, parent, usuario):
        super().__init__(parent)
        self.title(f"Sistema de Estoque - {usuario['nome']}")
        self.geometry("1100x750")
        self.usuario = usuario

        try:
            self.db = parent.db if hasattr(parent, 'db') else DBManager()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao conectar ao banco: {str(e)}")
            self.destroy()
            return

        self.style = ttk.Style()
        self.style.configure('TButton', font=('Arial', 10), padding=5)
        self.style.configure('Title.TLabel', font=('Arial', 14, 'bold'))
        self.style.configure('Subtitle.TLabel', font=('Arial', 12))
        self.style.configure('Alert.TLabel', font=('Arial', 10, 'bold'), foreground='red')

        self.criar_menu()
        self.criar_widgets_principal()
        self.protocol("WM_DELETE_WINDOW", self.fechar_aplicacao)
        self.center_window()

    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'+{x}+{y}')

    def criar_menu(self):
        menubar = tk.Menu(self)

        menu_cadastro = tk.Menu(menubar, tearoff=0)
        menu_cadastro.add_command(label="Usuários", command=self.abrir_cadastro_usuarios,
                                  state='normal' if self.usuario['nivel'] >= 2 else 'disabled')
        menu_cadastro.add_command(label="Fornecedores", command=self.abrir_cadastro_fornecedores)
        menu_cadastro.add_command(label="Produtos", command=self.abrir_cadastro_produtos)
        menu_cadastro.add_separator()
        menu_cadastro.add_command(label="Sair", command=self.fechar_aplicacao)
        menubar.add_cascade(label="Cadastros", menu=menu_cadastro)

        menu_estoque = tk.Menu(menubar, tearoff=0)
        menu_estoque.add_command(label="Movimentação", command=self.abrir_movimentacao_estoque)
        menu_estoque.add_command(label="Produtos", command=self.abrir_edicao_produtos)
        menu_estoque.add_command(label="Fornecedores", command=self.abrir_edicao_fornecedores)
        menubar.add_cascade(label="Estoque", menu=menu_estoque)

        menu_relatorios = tk.Menu(menubar, tearoff=0)
        menu_relatorios.add_command(label="Gerar Relatórios", command=self.abrir_relatorios)
        menu_relatorios.add_command(label="Estoque Baixo", command=self.mostrar_estoque_baixo)
        menu_relatorios.add_command(label="Movimentações", command=self.mostrar_movimentacoes)
        menubar.add_cascade(label="Relatórios", menu=menu_relatorios)

        menu_apis = tk.Menu(menubar, tearoff=0)
        menu_apis.add_command(label="Cotações de Moedas", command=self.abrir_cotacoes)
        menubar.add_cascade(label="APIs", menu=menu_apis)

        menu_ajuda = tk.Menu(menubar, tearoff=0)
        menu_ajuda.add_command(label="Sobre", command=self.mostrar_sobre)
        menu_ajuda.add_command(label="Manual", command=self.mostrar_manual)
        menubar.add_cascade(label="Ajuda", menu=menu_ajuda)

        self.config(menu=menubar)

    def criar_widgets_principal(self):
        main_frame = tk.Frame(self, padx=20, pady=20)
        main_frame.pack(expand=True, fill=tk.BOTH)

        # Cabeçalho
        header_frame = tk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 20))

        ttk.Label(
            header_frame,
            text=f"Bem-vindo, {self.usuario['nome']}",
            style='Title.TLabel'
        ).pack(side=tk.LEFT)

        ttk.Label(
            header_frame,
            text=f"Nível: {'Administrador' if self.usuario['nivel'] == 3 else 'Usuário' if self.usuario['nivel'] == 2 else 'Operador'}",
            style='Subtitle.TLabel'
        ).pack(side=tk.RIGHT)

        ttk.Label(
            main_frame,
            text="Sistema de Gerenciamento de Estoque",
            style='Subtitle.TLabel'
        ).pack(pady=(0, 20))

        btn_container = tk.Frame(main_frame)
        btn_container.pack(pady=10)

        btn_frame1 = tk.Frame(btn_container)
        btn_frame1.pack(pady=5)

        buttons_row1 = [
            ("Cadastrar Produto", self.abrir_cadastro_produtos),
            ("Cadastrar Fornecedor", self.abrir_cadastro_fornecedores),
            ("Movimentar Estoque", self.abrir_movimentacao_estoque)
        ]

        for text, command in buttons_row1:
            btn = ttk.Button(
                btn_frame1,
                text=text,
                command=command,
                width=20
            )
            btn.pack(side=tk.LEFT, padx=5, ipady=5)

        btn_frame2 = tk.Frame(btn_container)
        btn_frame2.pack(pady=5)

        buttons_row2 = [
            ("Editar Produtos", self.abrir_edicao_produtos),
            ("Editar Fornecedores", self.abrir_edicao_fornecedores),
            ("Relatórios", self.abrir_relatorios)
        ]

        for text, command in buttons_row2:
            btn = ttk.Button(
                btn_frame2,
                text=text,
                command=command,
                width=20
            )
            btn.pack(side=tk.LEFT, padx=5, ipady=5)

        if self.usuario['nivel'] >= 2:
            btn_frame3 = tk.Frame(btn_container)
            btn_frame3.pack(pady=5)

            buttons_row3 = [
                ("Cadastrar Usuário", self.abrir_cadastro_usuarios),
                ("Cotações", self.abrir_cotacoes),
                ("Estoque Baixo", self.mostrar_estoque_baixo)
            ]

            for text, command in buttons_row3:
                btn = ttk.Button(
                    btn_frame3,
                    text=text,
                    command=command,
                    width=20
                )
                btn.pack(side=tk.LEFT, padx=5, ipady=5)

        self.criar_secao_alertas(main_frame)

    def criar_secao_alertas(self, parent):
        alert_frame = tk.LabelFrame(parent, text=" Alertas do Sistema ", font=('Arial', 10, 'bold'), padx=10, pady=10)
        alert_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        try:
            produtos = self.db.buscar_produtos_baixo_estoque()

            if produtos:
                ttk.Label(
                    alert_frame,
                    text="Produtos com Estoque Abaixo do Mínimo",
                    style='Alert.TLabel'
                ).pack(anchor='w', pady=(0, 5))

                columns = ('id', 'nome', 'quantidade', 'estoque_minimo', 'fornecedor', 'status')
                tree = ttk.Treeview(alert_frame, columns=columns, show='headings', height=6)

                tree.heading('id', text='ID', anchor='center')
                tree.heading('nome', text='Nome do Produto')
                tree.heading('quantidade', text='Quantidade', anchor='center')
                tree.heading('estoque_minimo', text='Mínimo', anchor='center')
                tree.heading('fornecedor', text='Fornecedor')
                tree.heading('status', text='Status', anchor='center')

                tree.column('id', width=50, anchor='center')
                tree.column('nome', width=250)
                tree.column('quantidade', width=80, anchor='center')
                tree.column('estoque_minimo', width=80, anchor='center')
                tree.column('fornecedor', width=150)
                tree.column('status', width=100, anchor='center')

                for produto in produtos:
                    status = "CRÍTICO" if produto[2] == 0 else "ALERTA"
                    tree.insert('', 'end', values=(
                        produto[0],
                        produto[1],
                        produto[2],
                        produto[3],
                        produto[4] if produto[4] else "N/D",
                        status
                    ), tags=(status.lower(),))

                tree.tag_configure('crítico', background='#ffcccc')
                tree.tag_configure('alerta', background='#fff3cd')

                scrollbar = ttk.Scrollbar(alert_frame, orient=tk.VERTICAL, command=tree.yview)
                tree.configure(yscroll=scrollbar.set)

                tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
                scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

                btn_frame = tk.Frame(alert_frame)
                btn_frame.pack(fill=tk.X, pady=(5, 0))

                ttk.Button(
                    btn_frame,
                    text="Cadastrar Novo Produto",
                    command=self.abrir_cadastro_produtos,
                    style='TButton'
                ).pack(side=tk.RIGHT, padx=5)

            else:
                ttk.Label(
                    alert_frame,
                    text="Nenhum produto com estoque abaixo do mínimo",
                    style='Subtitle.TLabel'
                ).pack(expand=True, pady=50)

        except Exception as e:
            messagebox.showwarning("Aviso", f"Não foi possível carregar alertas: {str(e)}")

    def abrir_movimentacao_estoque(self):
        try:
            TelaMovimentacaoEstoque(self)
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível abrir a movimentação: {str(e)}")

    def mostrar_movimentacoes(self):
        try:
            movimentacoes = self.db.listar_movimentacoes()
            if movimentacoes:
                msg = "Últimas movimentações:\n\n"
                for mov in movimentacoes[:10]:  # Mostrar apenas as 10 mais recentes
                    msg += f"{mov[4]} - {mov[8]} ({mov[2].upper()}): {mov[3]} unidades\n"
                messagebox.showinfo("Movimentações", msg)
            else:
                messagebox.showinfo("Movimentações", "Nenhuma movimentação registrada")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao obter movimentações: {str(e)}")

    def mostrar_manual(self):
        messagebox.showinfo(
            "Manual do Sistema",
            "Manual do Sistema de Estoque\n\n"
            "1. Cadastros:\n"
            "   - Produtos: Cadastre todos os itens do estoque\n"
            "   - Fornecedores: Cadastre os fornecedores dos produtos\n"
            "   - Usuários: Gerencie os acessos ao sistema\n\n"
            "2. Movimentações:\n"
            "   - Registre entradas e saídas de produtos\n\n"
            "3. Relatórios:\n"
            "   - Gere relatórios de estoque e movimentações\n"
            "   - Verifique produtos com estoque baixo\n\n"
            "4. Configurações:\n"
            "   - Edite produtos e fornecedores existentes\n"
            "   - Consulte cotações de moedas"
        )

    def abrir_cadastro_produtos(self):
        try:
            TelaCadastroProduto(self)
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível abrir o cadastro de produtos: {str(e)}")

    def abrir_cadastro_fornecedores(self):
        try:
            TelaCadastroFornecedor(self)
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível abrir o cadastro de fornecedores: {str(e)}")

    def abrir_cadastro_usuarios(self):
        try:
            TelaCadastroUsuarios(self)
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível abrir o cadastro de usuários: {str(e)}")

    def abrir_edicao_produtos(self):
        try:
            TelaEdicaoProdutos(self)
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível abrir a edição de produtos: {str(e)}")

    def abrir_edicao_fornecedores(self):
        try:
            TelaEdicaoFornecedores(self)
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível abrir a edição de fornecedores: {str(e)}")

    def abrir_relatorios(self):
        try:
            TelaRelatorios(self)
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível abrir os relatórios: {str(e)}")

    def mostrar_estoque_baixo(self):
        try:
            produtos = self.db.buscar_produtos_baixo_estoque()
            if produtos:
                mensagem = "Produtos com estoque baixo:\n\n"
                for p in produtos:
                    status = "ESGOTADO" if p[2] == 0 else "BAIXO"
                    mensagem += f"{p[1]} (ID: {p[0]}) - Estoque: {p[2]} (Mínimo: {p[3]}) - {status}\n"
                messagebox.showinfo("Estoque Baixo", mensagem)
            else:
                messagebox.showinfo("Estoque Baixo", "Nenhum produto com estoque abaixo do mínimo")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao verificar estoque baixo: {str(e)}")

    def abrir_cotacoes(self):
        try:
            TelaCotacaoMoedas(self)
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível abrir as cotações: {str(e)}")

    def mostrar_sobre(self):
        messagebox.showinfo(
            "Sobre",
            "Sistema de Estoque v2.0\n\n"
            "Desenvolvido para controle de estoque\n"
            "Funcionalidades:\n"
            "- Cadastro de produtos e fornecedores\n"
            "- Controle de usuários\n"
            "- Relatórios e estoque mínimo\n"
            "- Movimentações de estoque\n"
            "- Integração com APIs externas"
        )

    def fechar_aplicacao(self):
        try:
            if hasattr(self, 'db') and self.db:
                self.db.fechar()
            self.master.deiconify()
            self.destroy()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao fechar a aplicação: {str(e)}")
            self.destroy()