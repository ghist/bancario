from historico import Historico
class Conta:
    
    __slots__ = ['_nome', '_cpf','_endereco','_nascimento', '_senha','_numero','_saldo']
    
    def __init__(self, nome, cpf, endereco, nascimento, senha, numero, saldo):
        self._nome = nome
        self._cpf = cpf
        self._endereco = endereco
        self._nascimento = nascimento
        self._senha = senha
        self._numero = numero
        self._saldo = saldo
        self._historico = Historico()
        
    def sacar(self, valor):
        if(self._saldo < valor):
            return False
        else:
            self._saldo -= valor
            self._historico._transacoes.append("saque de {}".format(valor))
            return True
        
    def depositar(self, valor):
        if(valor < 0):
            return False
        else:
            self._saldo += valor
            self._historico._transacoes.append("deposito de {}".format(valor))
            return True
        
    def transferir(self,valor,conta):
        retirou = self.sacar(valor)
        if(retirou == False):
            return False
        else:
            conta.depositar(valor)
            self._historico._transacoes.append("transferencia de {} para conta {}".format(valor, conta._numero))
