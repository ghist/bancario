import sys 
import os

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QMessageBox
from PyQt5.QtCore import QCoreApplication, QDate

from inicio_login import Tela_InicioLogin
from tela_cadastro import Tela_Cadastro
from tela_cliente import Tela_Cliente
from tela_deposito import Tela_Deposito
from tela_sacar import Tela_Sacar
from tela_transferir import Tela_Transferir

from clienteee import Conectar
from funcoes_auxiliares import concatenar_operacao


class Ui_Main(QtWidgets.QWidget):
    def setupUi(self, Main):
        Main.setObjectName('Main')
        Main.resize(640, 480)

        self.QtStack = QtWidgets.QStackedLayout()

        self.stack0 = QtWidgets.QMainWindow()
        self.stack1 = QtWidgets.QMainWindow()
        self.stack2 = QtWidgets.QMainWindow()
        self.stack3 = QtWidgets.QMainWindow()
        self.stack4 = QtWidgets.QMainWindow()
        self.stack5 = QtWidgets.QMainWindow()

        self.tela_inicial = Tela_InicioLogin()
        self.tela_inicial.setupUi(self.stack0)

        self.tela_cadastro = Tela_Cadastro()
        self.tela_cadastro.setupUi(self.stack1)

        self.tela_cliente = Tela_Cliente()
        self.tela_cliente.setupUi(self.stack2)

        self.tela_deposito = Tela_Deposito()
        self.tela_deposito.setupUi(self.stack3)

        self.tela_sacar = Tela_Sacar()
        self.tela_sacar.setupUi(self.stack4)

        self.tela_transferir = Tela_Transferir()
        self.tela_transferir.setupUi(self.stack5)

        self.QtStack.addWidget(self.stack0)
        self.QtStack.addWidget(self.stack1)
        self.QtStack.addWidget(self.stack2)
        self.QtStack.addWidget(self.stack3)
        self.QtStack.addWidget(self.stack4)
        self.QtStack.addWidget(self.stack5)

class Main(QMainWindow, Ui_Main):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setupUi(self)

        self.conectar_servidor = Conectar()

        
        self.tela_inicial.pushButton.clicked.connect(self.abrirTelaCliente)
        self.tela_inicial.pushButton_2.clicked.connect(self.abrirTelaCadastro)
        self.tela_inicial.pushButton_3.clicked.connect(self.sair)

        self.tela_cadastro.pushButton.clicked.connect(self.botaoCadastra)
        self.tela_cadastro.pushButton_2.clicked.connect(self.voltar)
        self.tela_cliente.pushButton.clicked.connect(self.botaoSacar)
        self.tela_cliente.pushButton_2.clicked.connect(self.botaoDepositar)
        self.tela_cliente.pushButton_3.clicked.connect(self.botaoTransferir)
        self.tela_cliente.pushButton_5.clicked.connect(self.voltar)
        self.tela_transferir.pushButton.clicked.connect(self.transferir)
        self.tela_transferir.pushButton_2.clicked.connect(self.voltar_cliente)
        self.tela_sacar.pushButton.clicked.connect(self.sacar)
        self.tela_sacar.pushButton_2.clicked.connect(self.voltar_cliente)
        self.tela_deposito.pushButton.clicked.connect(self.depositar)
        self.tela_deposito.pushButton_2.clicked.connect(self.voltar_cliente)


    def voltar(self):
        self.QtStack.setCurrentIndex(0)

    def voltar_cliente(self):
        self.QtStack.setCurrentIndex(2)
        
        mensagem = self.conectar_servidor.envia(concatenar_operacao(['9']))
        if(mensagem!=None):
            self.tela_cliente.lineEdit.setText(f'{mensagem[2]}')
            self.tela_cliente.lineEdit_2.setText(f'{mensagem[7]}')


    def sair(self):
        exit()

    def abrirTelaCadastro(self):
        self.QtStack.setCurrentIndex(1)

    def abrirTelaCliente(self):
        cpf = self.tela_inicial.lineEdit.text()
        senha = self.tela_inicial.lineEdit_2.text()

        if (cpf != '' and senha != ''):
            mensagem = self.conectar_servidor.envia(concatenar_operacao(['2', cpf, senha]))
            self.tela_inicial.lineEdit.setText('')
            self.tela_inicial.lineEdit_2.setText('')
            print(mensagem)
            if mensagem != None:
                if mensagem[0] == '0':
                    self.QtStack.setCurrentIndex(2)
                    QMessageBox.information(None, 'mensagem', mensagem[1])

                    self.tela_cliente.lineEdit.setText(f'{mensagem[3]}')
                    self.tela_cliente.lineEdit_2.setText(f'{mensagem[8]}')

                elif mensagem[0] == '1':
                    QMessageBox.information(None, 'mensagem', mensagem[1])
                    
                elif mensagem[0] == '2':
                    QMessageBox.information(None, 'mensagem', mensagem[1])
                    
                elif mensagem[0] == '3':
                    QMessageBox.information(None, 'mensagem', mensagem[1])
                
            else:
                QMessageBox.information(None, 'Login', 'Servidor fora do ar! Tente mais tarde...')
        else: QMessageBox.information(None, 'Login', 'Campos devem ser preenchidos!')

    def botaoCadastra(self):
        nome = self.tela_cadastro.lineEdit.text()
        cpf = self.tela_cadastro.lineEdit_2.text()
        endereco = self.tela_cadastro.lineEdit_3.text()
        nascimento = self.tela_cadastro.dateEdit.text()
        senha = self.tela_cadastro.lineEdit_4.text()
        numero = self.tela_cadastro.lineEdit_5.text()
        saldo = self.tela_cadastro.lineEdit_6.text()

        if not(nome == '' or cpf == '' or endereco == '' or senha == '' or numero == '' ):
            
            mensagem = self.conectar_servidor.envia(concatenar_operacao(['1',nome,cpf,endereco,nascimento,senha,numero,saldo]))

            QMessageBox.information(None, 'Cadastro', mensagem[1])
                
            self.tela_cadastro.lineEdit.setText('')
            self.tela_cadastro.lineEdit_2.setText('')
            self.tela_cadastro.lineEdit_3.setText('')
            self.tela_cadastro.lineEdit_4.setText('')
            self.tela_cadastro.lineEdit_5.setText('')
            self.tela_cadastro.lineEdit_6.setText('')


    def botaoSacar(self,):
        self.QtStack.setCurrentIndex(4)
        mensagem = self.conectar_servidor.envia(concatenar_operacao(['7']))
        if(mensagem!=None):
            self.tela_sacar.lineEdit.setText(f'{mensagem[7]}')

    def botaoDepositar(self):
        self.QtStack.setCurrentIndex(3)

    def botaoTransferir(self):
        self.QtStack.setCurrentIndex(5)
        mensagem = self.conectar_servidor.envia(concatenar_operacao(['7']))
        if(mensagem!=None):

            self.tela_transferir.lineEdit.setText(f'{mensagem[7]}')


    def sacar(self):
        valor_saq = self.tela_sacar.lineEdit_2.text()
        if not(valor_saq == ''):

            mensagem = self.conectar_servidor.envia(concatenar_operacao(['3', valor_saq]))
            if mensagem[0]== '0':
                QMessageBox.information(None, 'mensagem', mensagem[1])

                self.tela_sacar.lineEdit.setText(f'{mensagem[8]}')
            else:
                QMessageBox.information(None,"SAQUE", "Saque não Efetuado!")



    def depositar(self):
        valor = self.tela_deposito.lineEdit.text()
        if not(valor == ''):
            mensagem = self.conectar_servidor.envia(concatenar_operacao(['4', valor]))
            QMessageBox.information(None, 'mensagem', mensagem[1])
        

    def transferir(self):
        conta_destino = self.tela_transferir.lineEdit_3.text()
        valor = self.tela_transferir.lineEdit_2.text()
        if not ( conta_destino == '' or valor == '' ):
            mensagem = self.conectar_servidor.envia(concatenar_operacao(['5', conta_destino , valor]))

            if(mensagem[0]=='0'):
                QMessageBox.information(None, 'mensagem', mensagem[1])
                self.tela_transferir.lineEdit.setText(f'{mensagem[7]}')
            elif(mensagem[0]=='1'):
                QMessageBox.information(None, 'mensagem', mensagem[1])
            elif(mensagem[0]=='3'):
                QMessageBox.information(None, 'mensagem', mensagem[1])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    show_main = Main()
    sys.exit(app.exec_()) 