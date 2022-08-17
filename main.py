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
from cadastro import Cadastro
from conta import Conta
from historico import Historico

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

        self.QtStack.addWidget(self.stack0)
        self.QtStack.addWidget(self.stack1)
        self.QtStack.addWidget(self.stack2)
        self.QtStack.addWidget(self.stack3)
        self.QtStack.addWidget(self.stack4)

class Main(QMainWindow, Ui_Main):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setupUi(self)

        self.pessoa = None

        self.cad = Cadastro()
        self.tela_inicial.pushButton.clicked.connect(self.abrirTelaCliente)
        self.tela_inicial.pushButton_2.clicked.connect(self.abrirTelaCadastro)
        self.tela_inicial.pushButton_3.clicked.connect(self.sair)

        self.tela_cadastro.pushButton.clicked.connect(self.botaoCadastra)
        self.tela_cadastro.pushButton_2.clicked.connect(self.voltar)
        self.tela_cliente.pushButton.clicked.connect(self.botaoSacar)
        self.tela_cliente.pushButton_2.clicked.connect(self.botaoDepositar)
        self.tela_cliente.pushButton_5.clicked.connect(self.voltar)
        self.tela_sacar.pushButton.clicked.connect(self.sacar)
        self.tela_sacar.pushButton_2.clicked.connect(self.abrirTelaCliente)
        self.tela_deposito.pushButton.clicked.connect(self.depositar)
        self.tela_deposito.pushButton_2.clicked.connect(self.abrirTelaCliente)


    def voltar(self):
        self.QtStack.setCurrentIndex(0)

    def voltar_cliente(self):
        self.QtStack.setCurrentIndex(3)

    def sair(self):
        exit()

    def abrirTelaCadastro(self):
        self.QtStack.setCurrentIndex(1)

    def abrirTelaCliente(self):
        cpf = self.tela_inicial.lineEdit.text()
        senha = self.tela_inicial.lineEdit_2.text()
        pessoa = self.cad.login(cpf, senha)
        if(pessoa):
            self.QtStack.setCurrentIndex(2)
            self.tela_cliente.lineEdit.setText(pessoa['nome'])
            self.tela_cliente.lineEdit_2.setText(str(pessoa['saldo']))
            self.pessoa = pessoa

    def botaoCadastra(self):
        nome = self.tela_cadastro.lineEdit.text()
        cpf = self.tela_cadastro.lineEdit_2.text()
        endereco = self.tela_cadastro.lineEdit_3.text()
        nascimento = self.tela_cadastro.dateEdit.text()
        senha = self.tela_cadastro.lineEdit_4.text()
        numero = self.tela_cadastro.lineEdit_5.text()
        saldo = float(self.tela_cadastro.lineEdit_6.text())

        if not(nome == '' or cpf == '' or endereco == '' or senha == '' or numero == '' ):
            p = Conta(nome, cpf, endereco, nascimento, senha, numero, saldo)
            if(self.cad.cadastra(p)):
                QMessageBox.information(None, 'Cadastro', 'Cadastro realizado')
                self.tela_cadastro.lineEdit.setText('')
                self.tela_cadastro.lineEdit_2.setText('')
                self.tela_cadastro.lineEdit_3.setText('')
                self.tela_cadastro.lineEdit_4.setText('')
                self.tela_cadastro.lineEdit_5.setText('')
                self.tela_cadastro.lineEdit_6.setText('')
            else:
                QMessageBox.information(None, 'Cadastro', 'Cpf já cadastrado')
        else:
            QMessageBox.information(None, 'Cadastro', 'Valores em branco devem ser preenchidos')

    def botaoSacar(self,):
        self.QtStack.setCurrentIndex(4)
        self.tela_sacar.lineEdit.setText(str(self.pessoa['saldo']))

    def botaoDepositar(self):
        self.QtStack.setCurrentIndex(3)

    def sacar(self):
        valor = float(self.tela_sacar.lineEdit_2.text())
        saque = self.cad.sacar(self.pessoa, valor)
        if(saque == True):
            QMessageBox.information(None,"SAQUE", "Saque Efetuado!")
            self.QtStack.setCurrentIndex(4)
            self.tela_sacar.lineEdit.setText(str(self.pessoa['saldo']))
        else:
            QMessageBox.information(None,"SAQUE", "Saque não Efetuado!")


    def depositar(self):
        valor = float(self.tela_deposito.lineEdit.text())
        deposito = self.cad.depositar(self.pessoa, valor)
        if(deposito == True):
            QMessageBox.information(None,"DEPOSITO", "DEPOSITO Efetuado!")
            self.QtStack.setCurrentIndex(3)
        else:
            QMessageBox.information(None,"DEPOSITO", "DEPOSITO não Efetuado!")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    show_main = Main()
    sys.exit(app.exec_()) 