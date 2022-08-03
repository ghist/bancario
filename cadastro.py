class Cadastro:
    
    __slots__ = ['_lista_conta']

    def __init__(self):
        self._lista_conta = []

    def cadastra(self, conta):
        existe = self.busca(conta.cpf)
        if(existe == None):
            P = {'nome': conta.nome, 'cpf': conta.cpf, 'endereco': conta.endereco, 'nascimento': conta.nascimento,
                 'senha': conta.senha, 'numero': conta.numero, 'saldo': conta.saldo}
            self._lista_conta.append(P)
            print(self._lista_conta)
            return True
        else:
            return False

    def busca(self, cpf):
        for lp in self._lista_conta:
            if lp['cpf'] == cpf:
                return lp      
        return None

    def login(self, cpf, senha):
        for lp in self._lista_conta:
            if lp['cpf'] == cpf and lp['senha'] == senha:
                return lp
        return None