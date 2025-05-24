from hashlib import sha256

class Usuario:
    def __init__(self, nome, login, email, senha_hash):
        self.nome = nome
        self.login = login
        self.email = email
        self.senha_hash = senha_hash

    def validar_senha(self, senha):
        return self.senha_hash == sha256(senha.encode()).hexdigest()
