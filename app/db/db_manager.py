import sqlite3
from sqlite3 import Error

class DBManager:
    def __init__(self, db_file="app/db/estoque.db"):
        self.db_file = db_file
        self.con = None
        self.conectar()
        self.criar_tabelas()

    def conectar(self):
        try:
            self.con = sqlite3.connect(self.db_file)
        except Error as e:
            print(f"Erro ao conectar ao banco: {e}")

    def criar_tabelas(self):
        try:
            c = self.con.cursor()
            c.execute('''
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    login TEXT NOT NULL UNIQUE,
                    email TEXT,
                    senha TEXT NOT NULL,
                    nivel INTEGER NOT NULL
                )
            ''')

            c.execute('''
                CREATE TABLE IF NOT EXISTS fornecedores (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    contato TEXT,
                    telefone TEXT,
                    email TEXT
                )
            ''')

            c.execute('''
                CREATE TABLE IF NOT EXISTS produtos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    codigo TEXT UNIQUE,
                    descricao TEXT,
                    categoria TEXT,
                    fornecedor_id INTEGER,
                    quantidade INTEGER DEFAULT 0,
                    estoque_minimo INTEGER DEFAULT 0,
                    preco_custo REAL DEFAULT 0,
                    preco_venda REAL DEFAULT 0,
                    FOREIGN KEY(fornecedor_id) REFERENCES fornecedores(id)
                )
            ''')

            self.con.commit()
        except Error as e:
            print(f"Erro ao criar tabelas: {e}")

    # Usuários
    def inserir_usuario(self, nome, login, email, senha, nivel):
        c = self.con.cursor()
        c.execute("INSERT INTO usuarios (nome, login, email, senha, nivel) VALUES (?, ?, ?, ?, ?)",
                  (nome, login, email, senha, nivel))
        self.con.commit()

    def validar_login(self, login, senha):
        c = self.con.cursor()
        c.execute("SELECT * FROM usuarios WHERE login=? AND senha=?", (login, senha))
        return c.fetchone() is not None

    # Fornecedores
    def inserir_fornecedor(self, nome, contato, telefone, email):
        c = self.con.cursor()
        c.execute("INSERT INTO fornecedores (nome, contato, telefone, email) VALUES (?, ?, ?, ?)",
                  (nome, contato, telefone, email))
        self.con.commit()

    def listar_fornecedores(self):
        c = self.con.cursor()
        c.execute("SELECT id, nome, contato, telefone, email FROM fornecedores ORDER BY nome")
        return c.fetchall()

    # Produtos
    def inserir_produto(self, nome, codigo, descricao, categoria, fornecedor_id, quantidade, estoque_minimo, preco_custo, preco_venda):
        c = self.con.cursor()
        c.execute('''
            INSERT INTO produtos (nome, codigo, descricao, categoria, fornecedor_id, quantidade, estoque_minimo, preco_custo, preco_venda)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (nome, codigo, descricao, categoria, fornecedor_id, quantidade, estoque_minimo, preco_custo, preco_venda))
        self.con.commit()

    def produtos_estoque_baixo(self):
        c = self.con.cursor()
        c.execute("SELECT nome, quantidade, estoque_minimo FROM produtos WHERE quantidade <= estoque_minimo")
        return c.fetchall()

    def fechar(self):
        if self.con:
            self.con.close()
