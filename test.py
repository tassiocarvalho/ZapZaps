import socket
import threading
import sys
import json
import time

def get_local_ip_address(target='10.255.255.255'):
    """
    Função para obter o endereço IP local da máquina.
    Conecta-se a um endereço IP destino para determinar o endereço IP apropriado.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        try:
            # Não é necessário enviar dados, apenas iniciar a conexão
            s.connect((target, 1))
            IP = s.getsockname()[0]
        except Exception:
            IP = '127.0.0.1'
    return IP

local_ip = get_local_ip_address()

class UDPPeerChat:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.peers = []
        self.running = True
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.host, self.port))
        self.message_history = []  # Lista para armazenar o histórico de mensagens

    def start(self):
        threading.Thread(target=self.receive_messages).start()

    def add_peer(self, host, port):
        self.peers.append((host, port))

    def receive_messages(self):
        while self.running:
            try:
                data, addr = self.sock.recvfrom(1024)
                message = json.loads(data.decode())  # Desserializa a mensagem JSON
                formatted_message = f"Mensagem de {addr}: {message['text']}"
                self.message_history.append(formatted_message)
                self.display_chat_history()
                if addr not in self.peers:
                    self.peers.append(addr)
            except Exception as e:
                print(f"Erro ao receber mensagem: {e}")
                self.running = False

    def send_message(self, text):
        message = json.dumps({"sender": self.host, "text": text})  # Serializa em JSON
        self.message_history.append(f"Você: {text}")
        self.display_chat_history()
        for peer in self.peers:
            self.sock.sendto(message.encode(), peer)

    def display_chat_history(self):
        print("\n-------------- Histórico do Chat ----------------")
        for msg in self.message_history:
            print(msg)
        print("---------------------------------------------------\nobs: para sair digite /sair\n")

    def close(self):
        self.running = False
        self.sock.close()

if __name__ == "__main__":
    host = local_ip
    port = int(input("Seu IP é: "+local_ip+ " Digite a porta para este peer: "))
    chat = UDPPeerChat(host, port)
    chat.start()

    # Adicionar um peer externo
    ext_host = input("Digite o endereço IP de um peer externo (ou deixe em branco): ")
    if ext_host:
        ext_port = int(input("Digite a porta do peer externo: "))
        chat.add_peer(ext_host, ext_port)

    try:
        while True:
            message = input("Digite uma mensagem (ou 'sair' para sair): ")
            if message == '/sair':
                print("saindo...")
                time.sleep(2)
                sys.exit()
            else:
                chat.send_message(message)
    except KeyboardInterrupt:
        pass
    finally:
        chat.close()
