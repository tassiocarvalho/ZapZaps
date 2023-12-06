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
        self.peers = {}

    def add_peer(self):
        ip = input("Digite o IP do peer: ")
        port = int(input("Digite a porta do peer: "))
        new_peer = (ip, port)
        self.peers[new_peer] = "Desconhecido"
        self.send_message('join', f'{self.name} entrou no chat', new_peer)
        # Enviar mensagem de 'join' para todos os outros peers
        for peer in self.peers:
            if peer != new_peer:
                self.sock.sendto(json.dumps({"type": "join", "name": self.name}).encode(), peer)

    def start(self):
        print(f"Seu endereço IP local é: {get_local_ip_address()}")
        listener_thread = threading.Thread(target=self.listen_for_messages)
        listener_thread.daemon = True
        listener_thread.start()

        self.run_chat()

    def join_peer_chat(self):
        # Solicita ao usuário o IP e a porta do peer com o qual deseja conversar
        peer_ip = input("Digite o IP do peer para se conectar: ")
        peer_port = int(input("Digite a porta do peer: "))
        peer_address = (peer_ip, peer_port)

        # Adiciona o peer à lista de peers, se ainda não estiver lá
        if peer_address not in self.peers:
            self.peers[peer_address] = "Desconhecido"
            self.sock.sendto(json.dumps({"type": "join", "name": self.name}).encode(), peer_address)

        # Inicia a troca de mensagens com o peer específico
        while True:
            message = input(f"Digite sua mensagem para {peer_address} (ou 'exit' para sair): ")
            if message.lower() == 'exit':
                break
            self.send_message('chat', message, specific_peer=peer_address)

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

    def send_message(self, message_type, message, specific_peer=None):
        message_data = json.dumps({"type": message_type, "text": message, "name": self.name}).encode()
        if specific_peer:
            self.sock.sendto(message_data, specific_peer)
        else:
            for peer in self.peers:
                self.sock.sendto(message_data, peer)

    def add_peer(self):
        ip = input("Digite o IP do peer: ")
        port = int(input("Digite a porta do peer: "))
        self.peers[(ip, port)] = "Desconhecido"

    def run_chat(self):
        self.name = input("Digite seu nome: ")
        self.send_message('join', 'entrou no chat')
        print("\nEscolha \n[1] para adicionar um novo peer \n[2] para enviar mensagem direta \n[3] para aguardar por conexões \n[4] para sair.")

        while True:
            choice = input("\nOpção:")
            if choice == '1':
                self.add_peer()
            elif choice == '2':
                self.send_direct_message()
            elif choice == '3':
                print("Aguardando por novas mensagens ou conexões...")
                # Nada mais será feito aqui, continuará aguardando por mensagens no listener
            elif choice == '4':
                self.sock.close()
                sys.exit()
            else:
                self.send_message('chat', choice)

    def send_direct_message(self):
        print("Peers disponíveis:")
        for idx, peer in enumerate(self.peers):
            print(f"[{idx}] {self.peers[peer]} - {peer}")
        selected_idx = int(input("Selecione o número do peer: "))
        peer_key = list(self.peers.keys())[selected_idx]
        message = input("Digite sua mensagem: ")
        self.send_message('chat', message, specific_peer=peer_key)

if __name__ == "__main__":
    my_port = int(input("Digite sua porta: "))
    chat = P2PChat(my_port)
    chat.start()