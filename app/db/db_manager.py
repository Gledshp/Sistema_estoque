import sqlite3
from sqlite3 import Error

class DBManager:
    def __init__(self, db_estoque="app/db/estoque.db", db_usuarios="app/db/usuarios.db"):
        self.db_estoque = db_estoque
        self.db_usuarios = db_usuarios
        self.con_estoque = None
        self.con_usuarios = None

        self.connectar()
        self.criar_tabelas()

    def connectar(self):
        try:
            self.con_estoque = sqlite3.connect(self.db_estoque)
            self.con_estoque.execute("PRAGMA foreign_keys = ON")

            self.con_usuarios = sqlite3.connect(self.db_usuarios)

        except Error as e:
            print(f"Erro ao conectar aos bancos de dados: {e}")
            raise

    def criar_tabelas(self):
        try:
            c_estoque = self.con_estoque.cursor()

            c_estoque.execute('''
                CREATE TABLE IF NOT EXISTS fornecedores (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    contato TEXT,
                    telefone TEXT,
                    email TEXT
                )
            ''')

            c_estoque.execute('''
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
            c_usuarios = self.con_usuarios.cursor()

            c_usuarios.execute('''
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    login TEXT NOT NULL UNIQUE,
                    email TEXT,
                    senha TEXT NOT NULL,
                    nivel INTEGER NOT NULL
                )
            ''')

            self.con_estoque.commit()
            self.con_usuarios.commit()

        except Error as e:
            print(f"Erro ao criar tabelas: {e}")
            raise
    def inserir_usuario(self, nome, login, email, senha, nivel):
        try:
            c = self.con_usuarios.cursor()
            c.execute("""
                INSERT INTO usuarios (nome, login, email, senha, nivel) 
                VALUES (?, ?, ?, ?, ?)
            """, (nome, login, email, senha, nivel))
            self.con_usuarios.commit()
            return c.lastrowid
        except Error as e:
            print(f"Erro ao inserir usuário: {e}")
            raise

    def validar_login(self, login, senha):
        try:
            c = self.con_usuarios.cursor()
            c.execute("""
                SELECT * FROM usuarios 
                WHERE login=? AND senha=?
            """, (login, senha))
            return c.fetchone()
        except Error as e:
            print(f"Erro ao validar login: {e}")
            return None

    def inserir_fornecedor(self, nome, contato=None, telefone=None, email=None):
        try:
            c = self.con_estoque.cursor()
            c.execute("""
                INSERT INTO fornecedores (nome, contato, telefone, email) 
                VALUES (?, ?, ?, ?)
            """, (nome, contato, telefone, email))
            self.con_estoque.commit()
            return c.lastrowid
        except Error as e:
            print(f"Erro ao inserir fornecedor: {e}")
            raise
    def fechar(self):
        """Fecha ambas as conexões"""
        if self.con_estoque:
            self.con_estoque.close()
        if self.con_usuarios:
            self.con_usuarios.close()