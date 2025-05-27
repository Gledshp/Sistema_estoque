import pytest
from app.db.db_manager import DBManager


def test_inserir_produto_com_fornecedor_valido(tmp_path):
    db = DBManager(db_file=str(tmp_path / "test.db"))
    db.inserir_fornecedor("Fornecedor A", "contato", "1111", "teste@teste.com")

    produto_id = db.inserir_produto(
        nome="Notebook", codigo="NTB123", descricao="i5 8GB",
        categoria="Eletrônicos", fornecedor_id=1, quantidade=10,
        estoque_minimo=5, preco_custo=2500, preco_venda=3000
    )

    assert produto_id == 1  # Verifica se o produto foi criado
    db.fechar()