from operator import concat
from unittest import result
from classBanco import Banco
from funcoes_auxiliares import concatenar_operacao, replace_dados, v_int, v_float

import threading

class cliente_Thread(threading.Thread):

    def __init__(self, addr, socket, sinc):

        threading.Thread.__init__(self)
        self.conex = socket
        self.sinc = sinc
        self.ban = Banco()
        self.sessao = ''
        print(f"Nova conexao de: {addr}")

    def run(self):

        conexao = self.ban.criando_conexao(
            'localhost', 'root', '', 'banco')

        msg_recebida = ''
        while(msg_recebida != 'encerrar'):
            msg_recebida = self.conex.recv(1024).decode()
            if(msg_recebida == 'encerrar'):
                print("Cliente encerrado com sucesso! Aguardando novas conecxões...")
            else:
                print(f'{msg_recebida}')

            operacao = msg_recebida.split(',')

            if(operacao[0] == '1'):#cadastro usuario

                cpf = v_int(operacao[2])
                nome = str(operacao[1])
                endereco = str(operacao[3])
                nascimento = str(operacao[4])
                senha = operacao[5]
                numero = v_int(operacao[6])
                saldo = v_float(operacao[7])

                buscar = self.ban.Buscar_usuarios_bd(conexao, cpf)
                if(buscar == None):

                    inserindo_usuarios = f'INSERT INTO usuarios(cpf, nome, endereco, nascimento, senha, numero, saldo) VALUES ("{cpf}", "{nome}","{endereco}","{nascimento}","{senha}","{numero}","{saldo}")' 
                    self.ban.executando_query(conexao, inserindo_usuarios)
                    self.conex.send(
                        '0, Cadastro realizado com sucesso!'.encode())
                else:
                    self.conex.sendo('1, O cpf já está cadastrado!'.encode())
            
            elif(operacao[0] == '2'):#login
                cursor = conexao.cursor()
                cpf = operacao[1]
                valor = operacao[2]
                senha = valor
                self.sessao = cpf

                cursor.execute(
                    f"select * from usuarios where cpf = '{cpf}'")
                busca = cursor.fetchall()
                convert_lista = list(busca)

                if(convert_lista != ''):
                    if(convert_lista):
                        if((convert_lista[0][0] and convert_lista[0][4]) == (cpf and senha)):

                            resultado = self.ban.tratamento_dados(
                                conexao, self.sessao)
                            self.conex.send(('0, Login Realizado com Sucesso! ,' + resultado).encode())

                        else:
                            self.conex.send('1, Dados de login incorretos'.encode())

                else:
                    self.conex.send('3, Cliente nao cadastrado!'.encode())

            elif(operacao[0] == '3'):#sacar

                cursor = conexao.cursor()
                login = self.sessao
                valor_saq = v_float(operacao[1])

                self.sinc.acquire()
                cursor.execute(
                    f"select * from usuarios where cpf = '{login}'")
                valor = cursor.fetchall()
                convert_lista = list(valor)
                texto = str(valor_saq)

                if(convert_lista):
                    if((convert_lista[0][0]) == (login)):
                        conta = self.ban.Buscar_usuarios_bd(conexao, valor[0][0])

                        s = v_float(conta[0][6])

                        if(s >= valor_saq):
                            convert_conta = list(map(list, conta))

                            convert_conta[0][6] = (s - valor_saq)
                            alterar_saldo = (
                                f'UPDATE `banco`.`usuarios` SET saldo = {convert_conta[0][6]} WHERE (cpf = {conta[0][0]});')
                            self.ban.executando_query(conexao, alterar_saldo)
                            resultado = self.ban.tratamento_dados(
                                conexao, self.sessao)
                            self.conex.send(
                                ('0, Saque feito com sucesso!,' + resultado).encode())
                        else:
                            self.conex.send('1, Saldo insuficiente!'.encode())
                        self.sinc.release()

            elif(operacao[0] == '4'):#depositar

                login = self.sessao
                conta_dep = self.ban.Buscar_usuarios_bd_login(conexao, login)
                numero_conta = conta_dep[0][0]

                valor = v_float(operacao[1])
                self.sinc.acquire()

                c = self.ban.retorna_dado_conta(
                    conexao, 'cpf', 'cpf', numero_conta)
                saldo = self.ban.retorna_dado_conta(
                    conexao, 'saldo', 'cpf', numero_conta)
                list(saldo)
                if(c != None):
                    if not(c == None):

                        self.ban.altera_saldo(conexao, valor, c[0][0])
                        resultado = self.ban.tratamento_dados(
                            conexao, self.sessao)
                        self.conex.send(
                            ('0, Deposito feito com sucesso!,' + resultado).encode())
                self.sinc.release()
            
            elif(operacao[0] == '5'):#transferir
                conta_destino = v_int(operacao[1])
                valor = v_float(operacao[2])
                cs = self.sessao
                self.sinc.acquire()

                buscar_conta = self.ban.Buscar_usuarios_bd_login(conexao, cs)
                Buscar_conta_de_destino = self.ban.retorna_dado_conta(
                    conexao, 'cpf', 'cpf', conta_destino)
                if(Buscar_conta_de_destino):

                    if(buscar_conta[0][0] != None):

                        saldo = self.ban.transferirBD(conexao, Buscar_conta_de_destino[0][0], buscar_conta[0][0], valor)
                        if(saldo == True):
                            resultado = self.ban.tratamento_dados(conexao, self.sessao)
                            self.conex.send(('0, Transferencia feita com sucesso!,' + resultado).encode())
                        else:
                            self.conex.send(
                                '3, saldo insuficiente!,'.encode())
                    else:
                        self.conex.send('1, conta de destino nao existe'.encode())
                    self.sinc.release()
                
                # Abrir menu de de depositar
            elif(operacao[0] == '6'):  

                resultado = self.ban.tratamento_dados(conexao, self.sessao)
                self.conex.send(('0,' + resultado).encode())

            # Abrir menu de saque
            elif(operacao[0] == '7'):  

                resultado = self.ban.tratamento_dados(conexao, self.sessao)
                self.conex.send(('0,' + resultado).encode())

            # Abrir menu de transferir
            elif(operacao[0] == '8'):  

                resultado = self.ban.tratamento_dados(conexao, self.sessao)
                self.conex.send(('0,' + resultado).encode())

             # Botão VOltar para o menu
            elif(operacao[0] == '9'): 
                resultado = self.ban.tratamento_dados(conexao, self.sessao)
                self.conex.send(('0,' + resultado).encode())
            else:
                self.conex.send('1, Operação Inválida!'.encode())

        self.sessao = ''
        self.conex.send('1, Conexão Encerrada!!!'.encode())