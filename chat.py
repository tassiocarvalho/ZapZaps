import socket
import threading
import sys

# Configuração inicial
peer_ip = input("Digite o IP do par: ")
peer_port = int(input("Digite a porta do par: "))
my_port = int(input("Digite sua porta: "))

# Criar socket UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('', my_port))

def listen_for_messages():
    """Thread para escutar mensagens vindas de outros pares."""
    while True:
        data, addr = sock.recvfrom(1024)
        print("\nMensagem de {}: {}".format(addr, data.decode()))

def send_messages():
    """Função para enviar mensagens para o par."""
    while True:
        message = input()
        if message == 'quit':
            sock.close()
            sys.exit()
        sock.sendto(message.encode(), (peer_ip, peer_port))

# Iniciar a thread de escuta
listener_thread = threading.Thread(target=listen_for_messages)
listener_thread.daemon = True
listener_thread.start()

# Função principal para enviar mensagens
send_messages()
