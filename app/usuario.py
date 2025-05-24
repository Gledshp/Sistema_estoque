# Aqui você pode colocar as classes modelo se quiser. Por enquanto não é usado diretamente, pois usamos DBManager para acesso.
class Usuario:
    def __init__(self, id, nome, login, email, senha, nivel):
        self.id = id
        self.nome = nome
        self.login = login
        self.email = email
        self.senha = senha
        self.nivel = nivel
