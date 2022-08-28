from historico import Historico
import mysql.connector
class Cadastro:
    
    __slots__ = ['_lista_conta']

    def __init__(self):
        self._lista_conta = []

    def cadastra(self, conta):
        conexao = mysql.connector.connect(host='localhost', database='banco', user='root', passwd='')
        cursor = conexao.cursor()
        sql = """CREATE TABLE if NOT EXISTS usuarios(cpf VARCHAR(11) PRIMARY KEY, nome text NOT NULL, endereco text NOT NULL, nascimento VARCHAR(11) NOT NULL, senha VARCHAR(32) NOT NULL, numero VARCHAR(20) NOT NULL, saldo float NOT NULL);"""
        cursor.execute(sql)
        existe = self.busca(conta.cpf)
        if(existe == None):
            cursor.execute('INSERT INTO usuarios(cpf, nome, endereco, nascimento, senha, numero, saldo) VALUES (%s,%s,%s,%s,%s,%s,%s)', (conta.cpf, conta.nome, conta.endereco, conta.nascimento, conta.senha, conta.numero, conta.saldo))
            conexao.commit()
            conexao.close()
            return True
        else:
            conexao.commit()
            conexao.close()
            return False

    def busca(self, cpf):
        conexao = mysql.connector.connect(host='localhost', database='banco', user='root', passwd='')
        cursor = conexao.cursor()
        sql = "SELECT * FROM usuarios WHERE cpf = '{}'".format(cpf)
        cursor.execute(sql)
        sql1 = cursor.fetchone()
        print(sql1)
        if sql1 != None:
            return True
        else:
            return None

    def login(self, cpf, senha):
        conexao = mysql.connector.connect(host='localhost', database='banco', user='root', passwd='')
        cursor = conexao.cursor()
        cpf_v = "SELECT * FROM usuarios WHERE cpf ='{}'".format(cpf)
        cursor.execute(cpf_v)
        resultado = cursor.fetchone()
        print(resultado)
        if (resultado[0] == cpf) and (resultado[4] == senha):
            return resultado
        else:
            return None

    def sacar(self, conta, valor):
        conta = conta
        if(conta['saldo'] < float(valor)):
            return False
        else:
            conta['saldo'] -= float(valor)
            return True
        
    def depositar(self, conta, valor):
        conta = conta
        if(valor < 0):
            return False
        else:
            conta['saldo'] += float(valor)
            return True
        
    def transferir(self,valor,conta, conta1):
        conta2 = self.busca(conta1)
        retirou = self.sacar(conta, valor)
        if(retirou == False):
            return False
        else:
            self.depositar(conta2, valor)
            return True