import socket
import json
import threading
import os
import signal
import random
#from criptografia import Criptografia
import time
import platform
from vetorclock import VectorClock
user_clock = VectorClock(socket.gethostname())

#cripto = Criptografia()

# Flag para controlar quem responde à solicitação de histórico
should_respond_to_history_request = True

# Configurações de rede
broadcast_ip = '255.255.255.255'  # IP de broadcast
port = 12345  # Porta UDP

# Lista para armazenar mensagens e estado do chat
chat_store = []
in_chat = False  # Indica se o usuário está no chat
in_welcome_screen = False  # Indica se o usuário está na tela de boas-vindas

# Lock para sincronização
display_lock = threading.Lock()

received_messages = set()

# Inicializa o socket UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
sock.bind(('', port))

def signal_handler(sig, frame):
    print('Encerrando o chat...')
    sock.close()
    exit(0)

signal.signal(signal.SIGINT, signal_handler)

def clear_screen():
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')

def request_missing_messages():
    request_message = ('request_history', user_clock.as_dict())
    sock.sendto(json.dumps(request_message).encode(), (broadcast_ip, port))

def listen_for_messages():
    global in_chat, in_welcome_screen
    while True:
        try:
            data, addr = sock.recvfrom(4098)
            if data:
                received_message, received_data = json.loads(data.decode())
                if received_message == 'request_history':
                    respond_to_history_request(received_data, addr)
                elif received_message == 'history_response':
                    # Processar a resposta do histórico
                    for message in received_data:
                        message_id = (message[0], message[1], tuple(message[2].items()))
                        if message_id not in received_messages:
                            received_messages.add(message_id)
                            chat_store.append(message)
                else:
                    # Processar mensagens normais
                    user_clock.update(received_data)
                    message = (addr[0], received_message, user_clock.as_dict())
                    message_id = (addr[0], received_message, tuple(user_clock.as_dict().items()))
                    if message_id not in received_messages:
                        received_messages.add(message_id)
                        chat_store.append(message)
                    with display_lock:
                        if in_chat and not in_welcome_screen:
                            display_messages()
        except json.JSONDecodeError:
            print("Erro ao decodificar a mensagem recebida.")
            
def respond_to_history_request(requested_clock, addr):
    requested_vector_clock = VectorClock.from_dict(requested_clock, addr[0])
    if user_clock.is_after(requested_vector_clock):
        history_response = ('history_response', chat_store)
        sock.sendto(json.dumps(history_response).encode(), addr)

def display_messages():
    clear_screen()
    print("--------------BEM VINDO AO ZAPSZAP--------------")
    print("Digite '/menu' para retornar ao menu.\n")

    for message in chat_store:  # Exibe todas as mensagens
        addr, msg, clock = message
        print(f"{addr} falou: {msg} (Relógio: {clock})")
    print("\nEscreva sua mensagem: ", end='')

def send_message():
    global in_chat, in_welcome_screen
    in_chat = True
    in_welcome_screen = True

    clear_screen()
    print("--------------BEM VINDO AO ZAPSZAP--------------")
    print("Digite '/menu' para retornar ao menu.")
    print("APERTE ENTER PARA INICIAR O BATE PAPO:")
    input()  # Aguarda o usuário pressionar Enter antes de iniciar o bate-papo

    in_welcome_screen = False
    with display_lock:
        display_messages()

    while True:
        message = input()
        if message == '/menu':
            in_chat = False
            return
        elif message:
            user_clock.tick()  # Atualiza o relógio
            message_with_clock = (message, user_clock.as_dict())
            sock.sendto(json.dumps(message_with_clock).encode(), (broadcast_ip, port))
            with display_lock:
                display_messages()

def main_menu():
    global in_chat, in_welcome_screen
    while True:
        clear_screen()
        print("Bem-vindo ao ZAPSZAP")
        print("[1] Abrir chat.")
        print("[2] Sair.")

        choice = input("Escolha uma opção: ")

        if choice == '1':
            in_chat = True
            request_missing_messages()  # Solicitar mensagens perdidas
            send_message()
        elif choice == '2':
            break
        else:
            print("Opção inválida!")
            input("Pressione ENTER para continuar...")

# Thread para escutar mensagens
listener_thread = threading.Thread(target=listen_for_messages)
listener_thread.daemon = True
listener_thread.start()

# Menu principal
main_menu()