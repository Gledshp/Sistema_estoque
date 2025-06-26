import sqlite3
from sqlite3 import Error
import logging
from pathlib import Path
from hashlib import sha256


class DBManager:
    def __init__(self, db_estoque="estoque.db", db_usuarios="usuarios.db"):
        try:
            db_path = Path(__file__).parent.parent / "db"
            db_path.mkdir(exist_ok=True)

            self.db_estoque = str(db_path / db_estoque)
            self.db_usuarios = str(db_path / db_usuarios)
            self.con_estoque = None
            self.con_usuarios = None
            self.conectar()
            self.criar_tabelas()
        except Exception as e:
            logging.critical(f"Falha na inicialização do DBManager: {e}")
            raise RuntimeError(f"Erro ao inicializar DBManager: {e}")

    def conectar(self):
        try:
            self.con_estoque = sqlite3.connect(self.db_estoque)
            self.con_estoque.execute("PRAGMA foreign_keys = ON")
            self.con_usuarios = sqlite3.connect(self.db_usuarios)
            logging.info("Conexão com o banco de dados estabelecida")
        except Error as e:
            logging.critical(f"Falha na conexão: {e}")
            raise RuntimeError(f"Erro ao conectar aos bancos de dados: {e}")

    def criar_tabelas(self):
        try:
            c_estoque = self.con_estoque.cursor()

            # Tabela fornecedores com constraints de unicidade
            c_estoque.execute('''
                CREATE TABLE IF NOT EXISTS fornecedores (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL UNIQUE,
                    contato TEXT,
                    telefone TEXT,
                    email TEXT,
                    cnpj TEXT UNIQUE CHECK(length(cnpj) = 14 AND cnpj GLOB '[0-9]*'),
                    endereco TEXT,
                    data_cadastro TEXT DEFAULT CURRENT_TIMESTAMP
                )''')
            c_estoque.execute('''
                CREATE TABLE IF NOT EXISTS produtos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    codigo TEXT UNIQUE,
                    descricao TEXT,
                    categoria TEXT,
                    fornecedor_id INTEGER,
                    quantidade INTEGER DEFAULT 0 CHECK(quantidade >= 0),
                    estoque_minimo INTEGER DEFAULT 0 CHECK(estoque_minimo >= 0),
                    preco_custo REAL DEFAULT 0 CHECK(preco_custo >= 0),
                    preco_venda REAL DEFAULT 0 CHECK(preco_venda >= 0),
                    data_cadastro TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(fornecedor_id) REFERENCES fornecedores(id),
                    CHECK(preco_venda >= preco_custo)
                )''')

            # Tabela movimentações
            c_estoque.execute('''
                CREATE TABLE IF NOT EXISTS movimentacoes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    produto_id INTEGER NOT NULL,
                    tipo TEXT NOT NULL CHECK(tipo IN ('entrada', 'saida')),
                    quantidade INTEGER NOT NULL CHECK(quantidade > 0),
                    data TEXT DEFAULT CURRENT_TIMESTAMP,
                    usuario_id INTEGER,
                    observacao TEXT,
                    FOREIGN KEY(produto_id) REFERENCES produtos(id)
                )''')

            # Tabela usuários
            c_usuarios = self.con_usuarios.cursor()
            c_usuarios.execute('''
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    login TEXT NOT NULL UNIQUE,
                    email TEXT UNIQUE,
                    senha TEXT NOT NULL,
                    nivel INTEGER NOT NULL DEFAULT 1 CHECK(nivel IN (1, 2, 3)),
                    data_cadastro TEXT DEFAULT CURRENT_TIMESTAMP
                )''')

            # Criar usuário admin padrão se não existir
            c_usuarios.execute("SELECT * FROM usuarios WHERE login = 'admin'")
            if not c_usuarios.fetchone():
                senha_admin = sha256('admin123'.encode()).hexdigest()
                c_usuarios.execute('''
                    INSERT INTO usuarios (nome, login, senha, nivel)
                    VALUES (?, ?, ?, ?)
                ''', ('Administrador', 'admin', senha_admin, 3))

            self.con_estoque.commit()
            self.con_usuarios.commit()
            logging.info("Tabelas criadas com sucesso")
        except Error as e:
            self.con_estoque.rollback()
            self.con_usuarios.rollback()
            logging.error(f"Erro ao criar tabelas: {e}")
            raise RuntimeError("Falha na inicialização do banco de dados")

    # Métodos para usuários
    def validar_login(self, login, senha):
        try:
            if not login or not senha:
                raise ValueError("Login e senha são obrigatórios")

            c = self.con_usuarios.cursor()
            c.execute("SELECT * FROM usuarios WHERE login = ?", (login,))
            usuario = c.fetchone()

            if not usuario:
                logging.warning(f"Usuário não encontrado: {login}")
                raise ValueError("Credenciais inválidas")

            senha_hash = sha256(senha.encode()).hexdigest()
            if usuario[4] != senha_hash:
                logging.warning(f"Senha incorreta para usuário: {login}")
                raise ValueError("Credenciais inválidas")

            return {
                'id': usuario[0],
                'nome': usuario[1],
                'login': usuario[2],
                'email': usuario[3],
                'nivel': usuario[5]
            }
        except Error as e:
            logging.error(f"Erro ao validar login: {e}")
            raise RuntimeError("Falha na autenticação")

    def inserir_usuario(self, nome, login, email, senha, nivel):
        try:
            if not all([nome, login, senha]):
                raise ValueError("Nome, login e senha são obrigatórios")

            c = self.con_usuarios.cursor()
            c.execute('''
                INSERT INTO usuarios (nome, login, email, senha, nivel)
                VALUES (?, ?, ?, ?, ?)
            ''', (nome, login, email, senha, nivel))

            self.con_usuarios.commit()
            return c.lastrowid
        except sqlite3.IntegrityError as e:
            self.con_usuarios.rollback()
            if "UNIQUE constraint" in str(e):
                if "login" in str(e):
                    raise ValueError("Login já existe")
                elif "email" in str(e):
                    raise ValueError("Email já cadastrado")
            raise RuntimeError(f"Erro ao inserir usuário: {e}")
        except Error as e:
            self.con_usuarios.rollback()
            raise RuntimeError(f"Falha no cadastro de usuário: {e}")

    def verificar_fornecedor_existente(self, nome, cnpj=None):
        """Verifica se já existe um fornecedor com o mesmo nome ou CNPJ"""
        try:
            c = self.con_estoque.cursor()
            c.execute('SELECT COUNT(*) FROM fornecedores WHERE nome = ?', (nome,))
            if c.fetchone()[0] > 0:
                return True, "nome"
            if cnpj:
                c.execute('SELECT COUNT(*) FROM fornecedores WHERE cnpj = ?', (cnpj,))
                if c.fetchone()[0] > 0:
                    return True, "cnpj"

            return False, None

        except Error as e:
            logging.error(f"Erro ao verificar fornecedor existente: {e}")
            raise RuntimeError("Falha ao verificar fornecedor existente")

    def inserir_fornecedor(self, nome, contato=None, telefone=None, email=None, cnpj=None, endereco=None):
        try:
            if not nome:
                raise ValueError("Nome é obrigatório")

            if cnpj:
                if len(cnpj) != 14 or not cnpj.isdigit():
                    raise ValueError("CNPJ deve conter exatamente 14 dígitos numéricos")

            c = self.con_estoque.cursor()
            c.execute('''
                INSERT INTO fornecedores (nome, contato, telefone, email, cnpj, endereco)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (nome, contato, telefone, email, cnpj, endereco))

            self.con_estoque.commit()
            return c.lastrowid
        except sqlite3.IntegrityError as e:
            self.con_estoque.rollback()
            if "UNIQUE constraint" in str(e):
                if "cnpj" in str(e):
                    raise ValueError("CNPJ já cadastrado para outro fornecedor")
                elif "nome" in str(e):
                    raise ValueError("Já existe um fornecedor com este nome")
            raise RuntimeError(f"Erro ao inserir fornecedor: {e}")
        except Error as e:
            self.con_estoque.rollback()
            raise RuntimeError(f"Falha no cadastro de fornecedor: {e}")

    def atualizar_fornecedor(self, fornecedor_id, nome=None, contato=None, telefone=None,
                             email=None, cnpj=None, endereco=None):
        try:
            if not fornecedor_id:
                raise ValueError("ID do fornecedor é obrigatório")

            fornecedor = self.obter_fornecedor_por_id(fornecedor_id)
            if not fornecedor:
                raise ValueError("Fornecedor não encontrado")

            nome = nome if nome is not None else fornecedor[1]
            contato = contato if contato is not None else fornecedor[2]
            telefone = telefone if telefone is not None else fornecedor[3]
            email = email if email is not None else fornecedor[4]
            cnpj = cnpj if cnpj is not None else fornecedor[5]
            endereco = endereco if endereco is not None else fornecedor[6]

            if cnpj and (len(cnpj) != 14 or not cnpj.isdigit()):
                raise ValueError("CNPJ deve conter exatamente 14 dígitos numéricos")

            c = self.con_estoque.cursor()
            c.execute('''
                UPDATE fornecedores 
                SET nome = ?,
                    contato = ?,
                    telefone = ?,
                    email = ?,
                    cnpj = ?,
                    endereco = ?
                WHERE id = ?
            ''', (nome, contato, telefone, email, cnpj, endereco, fornecedor_id))

            self.con_estoque.commit()
            return c.rowcount
        except sqlite3.IntegrityError as e:
            self.con_estoque.rollback()
            if "UNIQUE constraint" in str(e):
                if "cnpj" in str(e):
                    raise ValueError("CNPJ já cadastrado para outro fornecedor")
                elif "nome" in str(e):
                    raise ValueError("Já existe um fornecedor com este nome")
            raise RuntimeError(f"Erro ao atualizar fornecedor: {e}")
        except Error as e:
            self.con_estoque.rollback()
            raise RuntimeError(f"Falha ao atualizar fornecedor: {e}")

    def listar_fornecedores(self, filtro=None):
        try:
            c = self.con_estoque.cursor()

            if filtro:
                query = '''
                    SELECT * FROM fornecedores 
                    WHERE nome LIKE ? OR cnpj LIKE ?
                    ORDER BY nome
                '''
                param = f"%{filtro}%"
                c.execute(query, (param, param))
            else:
                c.execute('SELECT * FROM fornecedores ORDER BY nome')

            return c.fetchall()
        except Error as e:
            logging.error(f"Erro ao listar fornecedores: {e}")
            raise RuntimeError("Falha ao recuperar lista de fornecedores")

    def consultar_cnpj(self, cnpj):
        try:
            if not cnpj or len(cnpj) != 14 or not cnpj.isdigit():
                raise ValueError("CNPJ deve conter exatamente 14 dígitos numéricos")

            c = self.con_estoque.cursor()
            c.execute('SELECT id, nome FROM fornecedores WHERE cnpj = ?', (cnpj,))
            fornecedor = c.fetchone()

            if fornecedor:
                return {
                    'existe': True,
                    'id': fornecedor[0],
                    'nome': fornecedor[1]
                }
            return {'existe': False}

        except ValueError as ve:
            raise ve
        except Error as e:
            logging.error(f"Erro ao consultar CNPJ: {e}")
            raise RuntimeError("Falha ao consultar CNPJ")

    def obter_fornecedor_por_id(self, fornecedor_id):
        try:
            c = self.con_estoque.cursor()
            c.execute('SELECT * FROM fornecedores WHERE id = ?', (fornecedor_id,))
            return c.fetchone()
        except Error as e:
            logging.error(f"Erro ao obter fornecedor: {e}")
            raise RuntimeError(f"Falha ao obter fornecedor: {e}")

    def eliminar_fornecedor(self, fornecedor_id):
        try:
            if not fornecedor_id:
                raise ValueError("ID do fornecedor é obrigatório")

            c = self.con_estoque.cursor()

            fornecedor = self.obter_fornecedor_por_id(fornecedor_id)
            if not fornecedor:
                raise ValueError("Fornecedor não encontrado")

            c.execute("SELECT COUNT(*) FROM produtos WHERE fornecedor_id = ?", (fornecedor_id,))
            count = c.fetchone()[0]

            if count > 0:
                raise ValueError("Não é possível eliminar fornecedor com produtos associados")

            c.execute("DELETE FROM fornecedores WHERE id = ?", (fornecedor_id,))
            self.con_estoque.commit()
            return c.rowcount
        except ValueError as ve:
            self.con_estoque.rollback()
            raise ve
        except Error as e:
            self.con_estoque.rollback()
            raise RuntimeError(f"Falha ao eliminar fornecedor: {e}")

    # Métodos para produtos
    def inserir_produto(self, nome, codigo, descricao=None, categoria=None, fornecedor_id=None,
                        quantidade=0, estoque_minimo=0, preco_custo=0, preco_venda=0):
        try:
            if not nome or not codigo:
                raise ValueError("Nome e código são obrigatórios")

            if fornecedor_id and not self.obter_fornecedor_por_id(fornecedor_id):
                raise ValueError("Fornecedor não encontrado")

            if preco_custo < 0 or preco_venda < 0 or estoque_minimo < 0 or quantidade < 0:
                raise ValueError("Valores não podem ser negativos")

            if preco_venda < preco_custo:
                raise ValueError("Preço de venda não pode ser menor que preço de custo")

            c = self.con_estoque.cursor()
            c.execute('''
                INSERT INTO produtos (nome, codigo, descricao, categoria, fornecedor_id,
                                    quantidade, estoque_minimo, preco_custo, preco_venda)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (nome, codigo, descricao, categoria, fornecedor_id,
                  quantidade, estoque_minimo, preco_custo, preco_venda))

            self.con_estoque.commit()
            return c.lastrowid
        except sqlite3.IntegrityError as e:
            self.con_estoque.rollback()
            if "UNIQUE constraint" in str(e):
                raise ValueError("Código do produto já existe")
            raise RuntimeError(f"Erro ao inserir produto: {e}")
        except Error as e:
            self.con_estoque.rollback()
            raise RuntimeError(f"Falha no cadastro de produto: {e}")

    def atualizar_produto(self, produto_id, nome=None, codigo=None, descricao=None, categoria=None,
                          fornecedor_id=None, quantidade=None, estoque_minimo=None,
                          preco_custo=None, preco_venda=None):
        try:
            if not produto_id:
                raise ValueError("ID do produto é obrigatório")

            produto = self.obter_produto_por_id(produto_id)
            if not produto:
                raise ValueError("Produto não encontrado")

            nome = nome if nome is not None else produto[1]
            codigo = codigo if codigo is not None else produto[2]
            descricao = descricao if descricao is not None else produto[3]
            categoria = categoria if categoria is not None else produto[4]
            fornecedor_id = fornecedor_id if fornecedor_id is not None else produto[5]
            quantidade = quantidade if quantidade is not None else produto[6]
            estoque_minimo = estoque_minimo if estoque_minimo is not None else produto[7]
            preco_custo = preco_custo if preco_custo is not None else produto[8]
            preco_venda = preco_venda if preco_venda is not None else produto[9]

            if preco_custo < 0 or preco_venda < 0 or estoque_minimo < 0 or quantidade < 0:
                raise ValueError("Valores não podem ser negativos")

            if preco_venda < preco_custo:
                raise ValueError("Preço de venda não pode ser menor que preço de custo")

            c = self.con_estoque.cursor()
            c.execute('''
                UPDATE produtos 
                SET nome = ?,
                    codigo = ?,
                    descricao = ?,
                    categoria = ?,
                    fornecedor_id = ?,
                    quantidade = ?,
                    estoque_minimo = ?,
                    preco_custo = ?,
                    preco_venda = ?
                WHERE id = ?
            ''', (nome, codigo, descricao, categoria, fornecedor_id,
                  quantidade, estoque_minimo, preco_custo, preco_venda, produto_id))

            self.con_estoque.commit()
            return c.rowcount
        except sqlite3.IntegrityError as e:
            self.con_estoque.rollback()
            if "UNIQUE constraint" in str(e):
                raise ValueError("Código do produto já existe")
            raise RuntimeError(f"Erro ao atualizar produto: {e}")
        except Error as e:
            self.con_estoque.rollback()
            raise RuntimeError(f"Falha ao atualizar produto: {e}")

    def listar_produtos(self, filtro=None):
        try:
            c = self.con_estoque.cursor()

            if filtro:
                query = '''
                    SELECT p.id, p.nome, p.codigo, p.quantidade, p.preco_venda, 
                           f.nome as fornecedor
                    FROM produtos p
                    LEFT JOIN fornecedores f ON p.fornecedor_id = f.id
                    WHERE p.nome LIKE ? OR p.codigo LIKE ? OR f.nome LIKE ?
                    ORDER BY p.nome
                '''
                param = f"%{filtro}%"
                c.execute(query, (param, param, param))
            else:
                c.execute('''
                    SELECT p.id, p.nome, p.codigo, p.quantidade, p.preco_venda, 
                           f.nome as fornecedor
                    FROM produtos p
                    LEFT JOIN fornecedores f ON p.fornecedor_id = f.id
                    ORDER BY p.nome
                ''')

            return c.fetchall()
        except Error as e:
            logging.error(f"Erro ao listar produtos: {e}")
            raise RuntimeError("Falha ao recuperar lista de produtos")

    def listar_produtos_relatorio(self, filtro=None):
        try:
            c = self.con_estoque.cursor()

            query = '''
                SELECT 
                    p.id, 
                    p.nome, 
                    p.quantidade, 
                    p.estoque_minimo,
                    CASE WHEN p.quantidade < p.estoque_minimo THEN 'ALERTA' ELSE 'Normal' END as status,
                    f.nome as fornecedor,
                    p.preco_venda
                FROM produtos p
                LEFT JOIN fornecedores f ON p.fornecedor_id = f.id
            '''

            params = ()
            if filtro:
                query += " WHERE p.nome LIKE ? OR p.codigo LIKE ? OR f.nome LIKE ?"
                param = f"%{filtro}%"
                params = (param, param, param)

            query += " ORDER BY p.nome"
            c.execute(query, params)

            return c.fetchall()
        except Error as e:
            logging.error(f"Erro ao listar produtos para relatório: {e}")
            raise RuntimeError("Falha ao recuperar lista de produtos para relatório")

    def obter_produto_por_id(self, produto_id):
        try:
            c = self.con_estoque.cursor()
            c.execute('''
                SELECT p.*, f.nome as fornecedor_nome 
                FROM produtos p
                LEFT JOIN fornecedores f ON p.fornecedor_id = f.id
                WHERE p.id = ?
            ''', (produto_id,))
            return c.fetchone()
        except Error as e:
            logging.error(f"Erro ao obter produto: {e}")
            raise RuntimeError(f"Falha ao obter produto: {e}")

    def obter_produto_por_codigo(self, codigo):
        try:
            c = self.con_estoque.cursor()
            c.execute('''
                SELECT p.*, f.nome as fornecedor_nome 
                FROM produtos p
                LEFT JOIN fornecedores f ON p.fornecedor_id = f.id
                WHERE p.codigo = ?
            ''', (codigo,))
            return c.fetchone()
        except Error as e:
            logging.error(f"Erro ao obter produto por código: {e}")
            raise RuntimeError(f"Falha ao obter produto por código: {e}")

    def verificar_produto_existente(self, nome_produto, fornecedor_id):
        try:
            c = self.con_estoque.cursor()
            c.execute('''
                SELECT COUNT(*) FROM produtos 
                WHERE nome = ? AND fornecedor_id = ?
            ''', (nome_produto, fornecedor_id))
            return c.fetchone()[0] > 0
        except Error as e:
            logging.error(f"Erro ao verificar produto existente: {e}")
            raise RuntimeError("Falha ao verificar produto existente")

    def obter_categorias_produtos(self):
        try:
            c = self.con_estoque.cursor()
            c.execute('''
                SELECT DISTINCT categoria FROM produtos 
                WHERE categoria IS NOT NULL AND categoria != ''
                ORDER BY categoria
            ''')
            return [row[0] for row in c.fetchall()]
        except Error as e:
            logging.error(f"Erro ao obter categorias de produtos: {e}")
            return []

    # Métodos para movimentações
    def registrar_movimentacao(self, produto_id, tipo, quantidade, usuario_id, observacao=None):
        try:
            if not produto_id or not tipo or not quantidade or not usuario_id:
                raise ValueError("Todos os campos são obrigatórios")

            if tipo not in ('entrada', 'saida'):
                raise ValueError("Tipo de movimentação inválido")

            if quantidade <= 0:
                raise ValueError("Quantidade deve ser maior que zero")

            c = self.con_estoque.cursor()

            produto = self.obter_produto_por_id(produto_id)
            if not produto:
                raise ValueError("Produto não encontrado")

            if tipo == "saida" and produto[6] < quantidade:
                raise ValueError("Estoque insuficiente para esta saída")

            if tipo == "entrada":
                c.execute('''
                    UPDATE produtos 
                    SET quantidade = quantidade + ?
                    WHERE id = ?
                ''', (quantidade, produto_id))
            else:
                c.execute('''
                    UPDATE produtos 
                    SET quantidade = quantidade - ?
                    WHERE id = ?
                ''', (quantidade, produto_id))

            c.execute('''
                INSERT INTO movimentacoes (produto_id, tipo, quantidade, usuario_id, observacao)
                VALUES (?, ?, ?, ?, ?)
            ''', (produto_id, tipo, quantidade, usuario_id, observacao))

            self.con_estoque.commit()
            return c.lastrowid
        except ValueError as ve:
            self.con_estoque.rollback()
            raise ve
        except Error as e:
            self.con_estoque.rollback()
            raise RuntimeError(f"Falha ao registrar movimentação: {e}")

    def listar_movimentacoes(self, produto_id=None, limite=100):
        try:
            c = self.con_estoque.cursor()

            if produto_id:
                c.execute('''
                    SELECT m.*, p.nome as produto, u.nome as usuario
                    FROM movimentacoes m
                    JOIN produtos p ON m.produto_id = p.id
                    LEFT JOIN usuarios u ON m.usuario_id = u.id
                    WHERE m.produto_id = ?
                    ORDER BY m.data DESC
                    LIMIT ?
                ''', (produto_id, limite))
            else:
                c.execute('''
                    SELECT m.*, p.nome as produto, u.nome as usuario
                    FROM movimentacoes m
                    JOIN produtos p ON m.produto_id = p.id
                    LEFT JOIN usuarios u ON m.usuario_id = u.id
                    ORDER BY m.data DESC
                    LIMIT ?
                ''', (limite,))

            return c.fetchall()
        except Error as e:
            logging.error(f"Erro ao listar movimentações: {e}")
            raise RuntimeError(f"Falha ao listar movimentações: {e}")

    def buscar_produtos_baixo_estoque(self):
        try:
            c = self.con_estoque.cursor()
            c.execute('''
                SELECT p.id, p.nome, p.quantidade, p.estoque_minimo, f.nome as fornecedor
                FROM produtos p
                LEFT JOIN fornecedores f ON p.fornecedor_id = f.id
                WHERE p.quantidade < p.estoque_minimo
                ORDER BY (p.quantidade * 1.0 / p.estoque_minimo) ASC
            ''')
            return c.fetchall()
        except Error as e:
            logging.error(f"Erro ao buscar produtos com baixo estoque: {e}")
            raise RuntimeError("Falha ao buscar produtos com baixo estoque")

    def eliminar_produto(self, produto_id):
        try:
            if not produto_id:
                raise ValueError("ID do produto é obrigatório")

            c = self.con_estoque.cursor()

            produto = self.obter_produto_por_id(produto_id)
            if not produto:
                raise ValueError("Produto não encontrado")

            c.execute("SELECT COUNT(*) FROM movimentacoes WHERE produto_id = ?", (produto_id,))
            count = c.fetchone()[0]

            if count > 0:
                raise ValueError("Não é possível eliminar produto com histórico de movimentações")

            c.execute("DELETE FROM produtos WHERE id = ?", (produto_id,))
            self.con_estoque.commit()
            return c.rowcount
        except ValueError as ve:
            self.con_estoque.rollback()
            raise ve
        except Error as e:
            self.con_estoque.rollback()
            raise RuntimeError(f"Falha ao eliminar produto: {e}")

    def fechar(self):
        try:
            if self.con_estoque:
                self.con_estoque.close()
            if self.con_usuarios:
                self.con_usuarios.close()
            logging.info("Conexões com o banco de dados fechadas")
        except Error as e:
            logging.error(f"Erro ao fechar conexões: {e}")
            raise RuntimeError(f"Erro ao fechar conexões com o banco: {e}")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.fechar()