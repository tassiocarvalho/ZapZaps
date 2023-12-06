import socket
import threading
import sys
import json

def get_local_ip_address(target='10.255.255.255'):
    """
    Função para obter o endereço IP local da máquina.
    Conecta-se a um endereço IP destino para determinar o endereço IP apropriado.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        try:
            s.connect((target, 1))
            IP = s.getsockname()[0]
        except Exception:
            IP = '127.0.0.1'
    return IP

class P2PChat:
    def __init__(self, my_port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('', my_port))
        self.peers = {}  # formato: {(ip, port): "nome"}

    def add_peer(self):
        ip = input("Digite o IP do peer: ")
        port = int(input("Digite a porta do peer: "))
        self.peers[(ip, port)] = "Desconhecido"
        # Enviar uma mensagem de 'join' para o novo peer
        self.sock.sendto(json.dumps({"type": "join", "name": self.name}).encode(), (ip, port))

    def start(self):
        print(f"Seu endereço IP local é: {get_local_ip_address()}")
        listener_thread = threading.Thread(target=self.listen_for_messages)
        listener_thread.daemon = True
        listener_thread.start()

        self.run_chat()

    def listen_for_messages(self):
        while True:
            try:
                data, addr = self.sock.recvfrom(1024)
                message = json.loads(data.decode())
                self.handle_message(addr, message)
            except Exception as e:
                print(f"Erro ao receber mensagem: {e}")

    def handle_message(self, addr, message):
        if message['type'] == 'join':
            self.peers[addr] = message['name']
            print(f"{message['name']} se juntou ao chat.")
        elif message['type'] == 'chat':
            print(f"{self.peers.get(addr, addr)}: {message['text']}")

    def send_message(self, message_type, message):
        message_data = json.dumps({"type": message_type, "text": message, "name": self.name}).encode()
        for peer in self.peers:
            self.sock.sendto(message_data, peer)

    def add_peer(self):
        ip = input("Digite o IP do peer: ")
        port = int(input("Digite a porta do peer: "))
        self.peers[(ip, port)] = "Desconhecido"

    def run_chat(self):
        self.name = input("Digite seu nome: ")
        self.send_message('join', 'entrou no chat')
        print("\nEscolha \n[1] para adicionar um novo peer \n[2] para aguardar por conexões \n[3] para sair.")

        while True:
            message = input("\nOpção:")
            if message == '1':
                self.add_peer()
            elif message == '2':
                print("Aguardandeo por novas mensagens ou conexões...")
                # Nada mais será feito aqui, continuará aguardando por mensagens no listener
            elif message == '3':
                self.sock.close()
                sys.exit()
            else:
                self.send_message('chat', message)

if __name__ == "__main__":
    my_port = int(input("Digite sua porta: "))
    chat = P2PChat(my_port)
    chat.start()