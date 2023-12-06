import socket
import threading
import json
import os
import platform
import sys

def clear_screen():
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')

class P2PChat:
    def __init__(self, my_port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('', my_port))
        self.peers = set()  # Conjunto de peers conectados
        self.message_history = []
        self.new_message_event = threading.Event()

    def update_screen(self):
        while True:
            if self.new_message_event.is_set():
                clear_screen()
                sys.stdout.write("\n" + "\n".join(self.message_history[-10:]))
                sys.stdout.flush()
                self.new_message_event.clear()
                
    def listen_for_messages(self):
        while True:
            try:
                data, addr = self.sock.recvfrom(1024)
                message = json.loads(data.decode())
                self.peers.add(addr)  # Adiciona o remetente aos peers, se ainda não estiver
                self.message_history.append(f"Mensagem de {addr}: {message['text']}")
                self.new_message_event.set()
            except Exception as e:
                print(f"Erro ao receber mensagem: {e}")

    def start_listening(self):
        listener_thread = threading.Thread(target=self.listen_for_messages, daemon=True)
        listener_thread.start()

    def send_message(self, message):
        for peer in self.peers:
            message_data = json.dumps({"text": message}).encode()
            self.sock.sendto(message_data, peer)
        self.message_history.append(f"Você: {message}")
        self.new_message_event.set()

    def set_peer(self, ip, port):
        self.peers.add((ip, port))

    def chat_mode(self):
        update_thread = threading.Thread(target=self.update_screen, daemon=True)
        update_thread.start()

        sys.stdout.write("\n" + "\n".join(self.message_history[-10:]))  # Exibe as últimas 10 mensagens
        sys.stdout.flush()

        while True:
            sys.stdout.write("\nEscreva sua mensagem (ou 'exit' para sair): ")
            sys.stdout.flush()
            message = input()
            if message.lower() == 'exit':
                break
            self.send_message(message)

    def wait_for_new_messages(self):
        while not self.new_message_event.is_set():
            # Não faz nada, apenas espera pelo próximo evento
            pass

        # Atualiza a tela com as novas mensagens
        clear_screen()
        sys.stdout.write("\n" + "\n".join(self.message_history[-10:]))
        sys.stdout.flush()

    def add_peer(self):
        ip = input("Digite o IP do peer: ")
        port = int(input("Digite a porta do peer: "))
        self.set_peer(ip, port)
        print(f"Peer adicionado: {ip}:{port}")

if __name__ == "__main__":
    my_port = int(input("Digite sua porta: "))
    chat = P2PChat(my_port)
    chat.start_listening()

    while True:
        clear_screen()  # Limpa a tela a cada iteração
        choice = input("\nEscolha [1] para aguardar conexão, [2] para conversar com o último peer, [3] para adicionar um peer: ")
        if choice == '1':
            print("Aguardando por mensagens...")
            chat.current_peer = None
            while chat.current_peer is None:
                pass  # Aguarda ativamente até que uma mensagem seja recebida
        elif choice == '2':
            if chat.current_peer:
                print(f"Conversando com {chat.current_peer}")
                chat.chat_mode()
            else:
                print("Nenhum peer para conversar. Aguarde uma mensagem.")
        elif choice == '3':
            chat.add_peer()
            chat.chat_mode()