import socket
import threading

from main_servidor import cliente_Thread


host = 'localhost'
porta = 8060

addr = (host,porta)

servidor = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #cria o socket e define o tipo de conexao e o tipo do protocolo de comunicaço
servidor.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1) #reinicializa o socket, para que possamos usar a porta novamente
servidor.bind(addr) #define o endereçõ do servidor
servidor.listen(10) #define o limite de conexao

print('\nAGUARDANDO CONEXAO...')

while True:
    conexao, cliente = servidor.accept()  # servidor aguarda uma conexao

    sinc = threading.Lock()
    Thread = cliente_Thread(cliente,conexao,sinc)
    Thread.start()
