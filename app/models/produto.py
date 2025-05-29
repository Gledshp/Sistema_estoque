class Produto:
    def __init__(self, id_, nome, codigo, descricao, categoria,
                 preco_compra, preco_venda, quantidade,
                 estoque_minimo, fornecedor):
        self._id = id_
        self._nome = nome
        self._codigo = codigo
        self._descricao = descricao
        self._categoria = categoria
        self._preco_compra = preco_compra
        self._preco_venda = preco_venda
        self._quantidade = quantidade
        self._estoque_minimo = estoque_minimo
        self._fornecedor = fornecedor

    @property
    def id(self):
        return self._id

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, value):
        self._nome = value

    @property
    def codigo(self):
        return self._codigo

    @codigo.setter
    def codigo(self, value):
        self._codigo = value

    @property
    def descricao(self):
        return self._descricao

    @descricao.setter
    def descricao(self, value):
        self._descricao = value

    @property
    def categoria(self):
        return self._categoria

    @categoria.setter
    def categoria(self, value):
        self._categoria = value

    @property
    def preco_compra(self):
        return self._preco_compra

    @preco_compra.setter
    def preco_compra(self, value):
        self._preco_compra = value

    @property
    def preco_venda(self):
        return self._preco_venda

    @preco_venda.setter
    def preco_venda(self, value):
        self._preco_venda = value

    @property
    def quantidade(self):
        return self._quantidade

    @quantidade.setter
    def quantidade(self, value):
        self._quantidade = value

    @property
    def estoque_minimo(self):
        return self._estoque_minimo

    @estoque_minimo.setter
    def estoque_minimo(self, value):
        self._estoque_minimo = value

    @property
    def fornecedor(self):
        return self._fornecedor

    @fornecedor.setter
    def fornecedor(self, value):
        self._fornecedor = value

    def __str__(self):
        return f"Produto(id={self._id}, nome='{self._nome}', codigo='{self._codigo}')"
