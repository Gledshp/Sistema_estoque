Sistema de Gerenciamento de Estoque
Este é um sistema completo para gerenciamento de estoque desenvolvido em Python com interface gráfica usando Tkinter e banco de dados SQLite.

Funcionalidades Principais
Cadastros
Produtos: Cadastro completo com código, descrição, categoria, preços e estoque mínimo

Fornecedores: Cadastro com CNPJ, contatos e endereço

Usuários: Sistema de autenticação com níveis de acesso (operador, usuário, administrador)

Movimentações
Entradas e saídas de estoque

Histórico completo de movimentações

Controle de estoque mínimo com alertas

Relatórios
Visualização de produtos com estoque baixo

Relatório geral de estoque

Histórico de movimentações

Integrações
Cotação de moedas (simulada)

Tecnologias Utilizadas
Python 3.x

Tkinter para interface gráfica

SQLite para banco de dados

Módulos Python:

sqlite3 para operações no banco de dados

hashlib para criptografia de senhas

logging para registro de eventos

pathlib para manipulação de caminhos de arquivos

Estrutura do Projeto
sistema_estoque/
├── .venv/                      # Ambiente virtual Python (opcional)
├── app/
│   ├── db/
│   │   ├── __init__.py         # Arquivo de inicialização do pacote
│   │   ├── db_manager.py       # Gerenciador principal do banco de dados
│   │   ├── estoque.db          # Banco de dados SQLite para estoque
│   │   └── usuarios.db         # Banco de dados SQLite para usuários
│   ├── interface/
│   │   ├── __init__.py         # Arquivo de inicialização
│   │   ├── estoque_errors.log  # Arquivo de log de erros
│   │   ├── tela_cadastro_fornecedores.py
│   │   ├── tela_cadastro_produtos.py
│   │   ├── tela_cadastro_usuarios.py
│   │   ├── tela_cotacao_moedas.py
│   │   ├── tela_edicao_fornecedores.py
│   │   ├── tela_edicao_produtos.py
│   │   ├── tela_login.py
│   │   ├── tela_movimentacao_estoque.py
│   │   ├── tela_principal.py
│   │   ├── tela_recuperar_senha.py
│   │   └── tela_relatorios.py
│   └── models/
│       ├── __init__.py         # Arquivo de inicialização
│       ├── fornecedor.py       # Modelo de fornecedor
│       ├── produto.py          # Modelo de produto
│       ├── usuario.py          # Modelo de usuário
│       └── venda.py            # Modelo de venda
├── data/
│   └── .gitkeep               # Arquivo para manter a pasta no git
├── sistema.db/                # Pasta com arquivos relacionados ao banco principal
│   ├── logs/
│   │   ├── estoque.log        # Logs gerais do sistema
│   │   └── estoque_errors.log # Logs de erros
│   └── test/
│       ├── features/
│       │   └── cadastro.feature.py  # Testes de comportamento
│       ├── integration/
│       │   └── test_tela_produto.py # Testes de integração
│       └── unit/
│           └── test_db_manager.py   # Testes unitários
├── __init__.py                # Inicialização do projeto
├── main.py                    # Ponto de entrada principal
└── requirements.txt           # Dependências do projeto
Como Executar
Certifique-se de ter Python 3.x instalado

Clone este repositório ou baixe os arquivos

Execute o arquivo principal:

bash
python main.py
Configuração Inicial
O sistema cria automaticamente:

Banco de dados estoque.db para os dados de produtos e fornecedores

Banco de dados usuarios.db para os dados de usuários

Um usuário administrador padrão:

Login: admin

Senha: admin123

Requisitos do Sistema
Python 3.6 ou superior

Módulos padrão do Python (não requer instalação adicional)

Licença
Este projeto está licenciado sob a licença MIT. Consulte o arquivo LICENSE para obter mais informações.
