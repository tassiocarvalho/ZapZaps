import socket
import threading
import sys
import json

# Configuração inicial
my_port = int(input("Digite sua porta: "))

# Criar socket UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('', my_port))

peer_ip = None
peer_port = None

def listen_for_messages():
    global peer_ip, peer_port
    """Thread para escutar mensagens vindas de outros pares."""
    while True:
        data, addr = sock.recvfrom(1024)
        message = json.loads(data.decode())
        if peer_ip is None or peer_port is None:
            peer_ip, peer_port = addr
            print(f"Conexão estabelecida com {peer_ip}:{peer_port}")
        print(f"\nMensagem de {addr}: {message['text']}")

def initiate_connection():
    global peer_ip, peer_port
    """Função para iniciar uma conexão com um par."""
    peer_ip = input("Digite o IP do par: ")
    peer_port = int(input("Digite a porta do par: "))
    print(f"Conectando a {peer_ip}:{peer_port}...")
    sock.sendto(json.dumps({'text': 'hello'}).encode(), (peer_ip, peer_port))

def send_messages():
    """Função para enviar mensagens para o par."""
    while True:
        message = input()
        if message == 'quit':
            sock.close()
            sys.exit()
        if peer_ip is not None and peer_port is not None:
            sock.sendto(json.dumps({'text': message}).encode(), (peer_ip, peer_port))
        else:
            print("Aguardando conexão do par...")

# Iniciar a thread de escuta
listener_thread = threading.Thread(target=listen_for_messages)
listener_thread.daemon = True
listener_thread.start()

# Perguntar se deseja iniciar uma conexão
if input("Deseja iniciar uma conexão? (s/n): ").lower() == 's':
    initiate_connection()

# Função principal para enviar mensagens
send_messages()
