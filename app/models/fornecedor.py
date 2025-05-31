class Fornecedor:
    def __init__(self, id_, nome, contato=None, telefone=None, email=None):
        self._id = id_
        self._nome = nome
        self._contato = contato
        self._telefone = telefone
        self._email = email
        self._endereco = endereco

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
    def contato(self):
        return self._contato

    @contato.setter
    def contato(self, value):
        self._contato = value

    @property
    def telefone(self):
        return self._telefone

    @telefone.setter
    def telefone(self, value):
        self._telefone = value

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        self._email = value

    @property
    def endereco(self):
    return self._endereco

    @endereco.setter
    def endereco(self, value):
        self._endereco = value

    def __str__(self):
        return f"Fornecedor(id={self._id}, nome='{self._nome}')"
