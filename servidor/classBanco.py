from unittest import result
import mysql.connector
from mysql.connector import Error

import datetime
from funcoes_auxiliares import concatenar_operacao, replace_dados, v_int, v_float

class Banco:

    def criando_conexao(self, host_name, user_name, user_passwd, db_name):
        self.conexao = None
        try:
            self.conexao = mysql.connector.connect(
                host=host_name,
                user=user_name,
                passwd=user_passwd,
                database=db_name
            )
            print("Conection Sucessful")
        except Error as err:
            print(f"Error: '{err}'")
        return self.conexao
    
    def criando_bancodedados(self, conexao, query):
        self.cursor=conexao.cursor()
        try:
            self.cursor.execute(query)
            print("Banco de dados criado com sucesso!")
        except Error as err:
            print(f"Error: '{err}'")

    def executando_query(self, conexao, query):
        self.cursor = conexao.cursor()
        try:
            self.cursor.execute(query)
            conexao.commit()
            print("SQL executada!")
        except Error as err:
            print(f"Error: ''{err}'")

    def lendo_dados(self, conexao, query):
        self.cursor = conexao.cursor()
        self.result = None
        try:
            self.cursor.execute(query)
            self.result = self.cursor.fetchall()
            return self.result
        except Error as err:
            print(f"Error: '{err}'")
        
    def Buscar_usuarios_bd(self, conexao, cpf):
        self.cursor = conexao.cursor()

        self.cursor.execute(
            f'SELECT * FROM usuarios WHERE cpf = {cpf}')
        resultado = self.cursor.fetchall()

        if resultado:
            return list(resultado)
        else:
            None

    def Buscar_usuarios_bd_login(self, conexao, login):
        self.cursor = conexao.cursor()

        self.cursor.execute(
            f"SELECT * FROM usuarios WHERE cpf = {login}")
        resultado = self.cursor.fetchall()

        if resultado:
            return list(resultado)
        else:
            None

    def logar_conta(self, conexao, cpf, senha):
        self.cursor = conexao.cursor()
        self.cursor.execute(
            f"select * from usuarios where cpf = '{cpf}' and senha = '{senha}'")
        valor = self.cursor.fetchall()
        print(valor)
    
    def altera_saldo(self, conexao, novo_valor, chave_de_busca):
        self.cursor = conexao.cursor()
        self.cursor.execute(
            f'SELECT * FROM usuarios WHERE cpf = {chave_de_busca}')
        resultado = self.cursor.fetchall()
        list(resultado)
        saldo2 = self.retorna_dado_conta(
            conexao, 'saldo', 'cpf', chave_de_busca)
        float(saldo2[0][0])
        teste = saldo2[0][0]
        float(novo_valor)

        teste += novo_valor

        self.cursor.execute(f'Update `banco`.`usuarios` SET saldo ={teste} WHERE (cpf = {chave_de_busca});')

        self.conexao.commit()

    def criar_Banco(self):

        database_query = "CREATE DATABASE IF NOT EXISTS banco"
        conexao = self.criando_conexao('localhost', 'root', '', 'banco')

        self.criando_bancodedados(conexao, database_query) 

        tabela_usuarios = "CREATE TABLE if NOT EXISTS usuarios(cpf VARCHAR(11) PRIMARY KEY, nome text NOT NULL, endereco text NOT NULL, nascimento VARCHAR(11) NOT NULL, senha VARCHAR(32) NOT NULL, numero VARCHAR(20) NOT NULL, saldo float(5,2) NOT NULL);"
        self.executando_query(conexao, tabela_usuarios)

    def retorna_dado_conta(self,  conexao, dado, atributo, parametro):
        self.cursor = conexao.cursor()

        self.cursor.execute(
            f'select {dado} from usuarios where {atributo} = {parametro}')

        valor = self.cursor.fetchall()
        print(valor)

        if valor == []:
            return None
        else:
            return list(valor)

    def transferirBD(self, conexao, destino, saida, valor):
        self.cursor = conexao.cursor()

        self.altera_saldo(conexao, valor, destino)

        self.cursor.execute(
            f'SELECT * FROM usuarios WHERE cpf = {saida}')
        resultado = self.cursor.fetchall()
        list(resultado)
        saldo2 = self.retorna_dado_conta(
            conexao, 'saldo', 'cpf', saida)
        float(saldo2[0][0])
        teste = saldo2[0][0]
        float(valor)


        if(valor>teste):
            return False
        elif(valor<teste):
            teste -= valor

            self.cursor.execute(
                f'UPDATE `banco`.`usuarios` SET saldo = {teste} WHERE (cpf = {saida});')
            self.conexao.commit()
            return True

        

    def altera_saldo2(self, conexao, query):
        self.cursor = conexao.cursor()
        altera_saldo = query
        try:
            self.cursor.execute(altera_saldo)
            self.conexao.commit()
            print("Saldo alterado com sucesso")
        except Error as err:
            print(f"Error: '{err}'")

    def tratamento_dados(self, conexao, user):
        login = user

        q1 = (f"select * from usuarios where cpf = '{login}'")
        dados = self.lendo_dados(conexao, q1)
        lista = list(dados)
        busca_conta = self.Buscar_usuarios_bd_login(conexao, login)
        cli = concatenar_operacao(lista)
        con = concatenar_operacao(busca_conta)
        resu_cli = replace_dados(cli)
        resu_con = replace_dados(con)
        resultado = resu_cli + resu_con
        return resultado