class Venda:
    def __init__(self, id_, produto_id, quantidade, data):
        self._id = id_
        self._produto_id = produto_id
        self._quantidade = quantidade
        self._data = data

    @property
    def id(self):
        return self._id

    @property
    def produto_id(self):
        return self._produto_id

    @property
    def quantidade(self):
        return self._quantidade

    @property
    def data(self):
        return self._data

    def __str__(self):
        return f"Venda(id={self._id}, produto_id={self._produto_id}, quantidade={self._quantidade}, data='{self._data}')"
