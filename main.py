import sys 
import os

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from PyQt5.QtCore import QCoreApplication

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
        self.QtStack.setCurrentIndex(2)

    def botaoCadastra(self):
        pass

    def botaoSacar(self):
        self.QtStack.setCurrentIndex(4)

    def botaoDepositar(self):
        self.QtStack.setCurrentIndex(3)

    def sacar(self):
        pass

    def depositar(self):
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    show_main = Main()
    sys.exit(app.exec_()) 