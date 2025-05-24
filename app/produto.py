class Produto:
    def __init__(self, id, nome, codigo, descricao, categoria, preco_compra, preco_venda, quantidade, estoque_minimo, fornecedor_id):
        self.id = id
        self.nome = nome
        self.codigo = codigo
        self.descricao = descricao
        self.categoria = categoria
        self.preco_compra = preco_compra
        self.preco_venda = preco_venda
        self.quantidade = quantidade
        self.estoque_minimo = estoque_minimo
        self.fornecedor_id = fornecedor_id
