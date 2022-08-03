import datetime

class Historico:
    def __init__(self):
        self._data_abertura = datetime.datetime.today()
        self._transacoes = []
        
    def imprimir(self):
        print("data abertura: {}".format(self._data_abertura))
        print("transações")
        for t in self._transacoes:
            print("-",t)