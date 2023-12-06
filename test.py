import socket
import threading
import sys
import json
import time
import os

def clear_screen():
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')

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

class Group:
    def __init__(self, name):
        self.name = name
        self.members = []

    def add_member(self, member_addr):
        if member_addr not in self.members:
            self.members.append(member_addr)

    def remove_member(self, member_addr):
        if member_addr in self.members:
            self.members.remove(member_addr)

    def get_members(self):
        return self.members

class UDPPeerChat:
    def __init__(self, host, port, group_name):
        self.host = host
        self.port = port
        self.group = Group(group_name)  # Criar um grupo
        self.peers = []  # Inicializar a lista de peers
        self.running = True
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.host, self.port))
        self.message_history = []

    def start(self):
        threading.Thread(target=self.receive_messages).start()

    def add_peer(self, host, port):
        peer_addr = (host, port)
        self.group.add_member(peer_addr)  # Adicionar membro ao grupo
        if peer_addr not in self.peers:
            self.peers.append(peer_addr)
            # Enviar mensagem de aviso sobre novo peer
            join_message = f"{peer_addr} entrou na conversa"
            self.broadcast_system_message(join_message)

    def broadcast_system_message(self, message):
        # Envia uma mensagem do sistema para todos os membros do grupo
        for peer in self.group.get_members():
            system_message = json.dumps({"system": True, "text": message})
            self.sock.sendto(system_message.encode(), peer)

    def handle_command(self, command):
        parts = command.split()
        if parts[0] == "/add_member":
            if len(parts) != 3:
                print("Uso correto: /add_member <IP> <porta>")
                return
            _, ip, port = parts
            try:
                self.add_peer(ip, int(port))
                print(f"Peer {ip}:{port} adicionado ao grupo.")
            except ValueError:
                print("Endereço IP ou porta inválidos.")

    def receive_messages(self):
        while self.running:
            try:
                data, addr = self.sock.recvfrom(1024)
                message = json.loads(data.decode())

                if 'system' in message and message['system']:
                    system_message = f"{message['text']}"
                    self.message_history.append(system_message)
                    self.display_chat_history()

                    # Adicionar lógica para tratar mensagens de novo peer aqui

                else:
                    # Tratamento para mensagens comuns
                    formatted_message = f"Mensagem de {addr}: {message['text']}"
                    self.message_history.append(formatted_message)
                    self.display_chat_history()

            except Exception as e:
                print(f"Erro ao receber mensagem: {e}")
                self.running = False

    def send_message(self, text):
        if text.startswith("/"):
            self.handle_command(text)
        else:
            message = json.dumps({"sender": self.host, "text": text})
            self.message_history.append(f"Você: {text}")
            self.display_chat_history()
            for peer in self.group.get_members():
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
    port = int(input("Seu IP é: " + local_ip + " Digite a porta para este peer: "))
    group_name = input("Digite o nome do grupo: ")
    chat = UDPPeerChat(host, port, group_name)
    chat.start()

    # Adicionar um peer externo
    ext_host = input("Digite o endereço IP de um peer externo (ou deixe em branco): ")
    if ext_host:
        ext_port = int(input("Digite a porta do peer externo: "))
        chat.add_peer(ext_host, ext_port)

    try:
        while True:
            message = input("Digite uma mensagem ou comando: ")
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
