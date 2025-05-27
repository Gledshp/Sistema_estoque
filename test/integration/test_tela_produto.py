from unittest.mock import MagicMock, patch
from app.interface.tela_cadastro_produtos import TelaCadastroProdutos

def test_cadastro_sem_nome_exibe_alerta():
    with patch('tkinter.messagebox.showwarning') as mock_msg:
        tela = TelaCadastroProdutos()
        tela.db = MagicMock()
        tela.cadastrar_produto()  # Campos vazios
