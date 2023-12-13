import socket
import struct
import threading
import os
import platform
import json
from threading import Lock
import vetorclock
from criptografia import generate_keys, serialize_public_key, deserialize_public_key, encrypt_message, decrypt_message

# Configurações do multicast
multicast_group = '224.0.0.2'
port = 12345

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

# Inicializa o socket UDP para recebimento de mensagens multicast
recv_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
recv_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
recv_sock.bind(('', port))

# Configuração do TTL para pacotes multicast
ttl = struct.pack('b', 1)  # TTL = 1 para redes locais
recv_sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

# Solicitar ao sistema operacional para adicionar o socket ao grupo multicast
group = socket.inet_aton(multicast_group)
local_interface = socket.inet_aton(local_ip)
mreq = struct.pack('4s4s', group, local_interface)
recv_sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

# Inicializa o socket UDP para envio de mensagens multicast
send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
send_sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

# Lista para armazenar mensagens
chat_history = []
chat_history_lock = Lock()
first_time = True

public_keys = {}
private_key = None

def share_public_key():
    """
    Compartilha a chave pública do usuário com outros usuários no chat.
    """
    public_key = private_key.public_key()
    public_key_serialized = serialize_public_key(public_key)

    public_key_message = {
        "ip": local_ip,
        "type": "public_key",
        "public_key": public_key_serialized.decode()
    }
    send_sock.sendto(json.dumps(public_key_message).encode(), (multicast_group, port))

def clear_screen():
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')

def update_and_display_chat_history():
    with chat_history_lock:
        clear_screen()
        for message in chat_history:
            print(message)

def send_chat_history(new_user_ip):
    """
    Envia todo o histórico de mensagens como uma única mensagem especial.
    :param new_user_ip: Endereço IP do novo usuário.
    """
    with chat_history_lock:
        history_message = {
            "ip": local_ip,
            "type": "history",  # Adiciona um tipo para identificar a mensagem como histórico
            "history": chat_history
        }
        send_sock.sendto(json.dumps(history_message).encode(), (new_user_ip, port))

is_responsible_for_history = False

def listen_for_messages(vclock):
    global is_responsible_for_history
    local_ip = get_local_ip_address()

    while True:
        data, addr = recv_sock.recvfrom(4096)
        message_json = data.decode()
        message = json.loads(message_json)

        if message.get("type") == "public_key" and message["ip"] != local_ip:
            public_key_serialized = message["public_key"].encode()
            public_keys[message["ip"]] = deserialize_public_key(public_key_serialized)

        # Verificando se é uma solicitação de chaves públicas
        elif message.get("type") == "request_public_keys" and message["ip"] != local_ip:
            # Responde à solicitação de chaves públicas
            share_public_key()

        elif message["ip"] != local_ip:
            if message.get("type") == "history":
                with chat_history_lock:
                    chat_history.extend(message["history"])
                is_responsible_for_history = False
            elif message.get("message") == "new_user_connected":
                if is_responsible_for_history:
                    send_chat_history(addr[0])
            elif 'encrypted_message' in message:
                encrypted_message = bytes.fromhex(message["encrypted_message"])
                decrypted_message = decrypt_message(private_key, encrypted_message)

                formatted_message = f"{message['ip']} falou: {decrypted_message}"
                with chat_history_lock:
                    chat_history.append(formatted_message)
                    print('\r' + formatted_message + "\nEscreva sua mensagem: ", end='', flush=True)

def send_message(vclock):
    global first_time, is_responsible_for_history
    local_ip = get_local_ip_address()

    if first_time:
        # Compartilha a chave pública ao entrar no chat
        share_public_key()

        # Assumindo inicialmente a responsabilidade pelo histórico
        is_responsible_for_history = True

        # Envia uma mensagem especial para indicar que é um novo usuário
        special_message = {
            "ip": local_ip,
            "message": "new_user_connected",
            "vclock": vclock.timestamps
        }
        send_sock.sendto(json.dumps(special_message).encode(), (multicast_group, port))
        first_time = False

    while True:
        message_text = input("\nEscreva sua mensagem: ")
        if message_text.strip():
            vclock.increment(local_ip)
            for ip, pub_key in public_keys.items():
                if ip != local_ip:
                    encrypted_message = encrypt_message(pub_key, message_text)
                    hex_encrypted_message = encrypted_message.hex()
                    message = {
                        "ip": local_ip,
                        "encrypted_message": hex_encrypted_message,
                        "vclock": vclock.timestamps
                    }
                    send_sock.sendto(json.dumps(message).encode(), (ip, port))

            with chat_history_lock:
                chat_history.append(f"{local_ip} falou: {message_text}")
            update_and_display_chat_history()

def main_menu():
    global private_key
    vclock = vetorclock.VectorClock()

    private_key, _ = generate_keys()
    share_public_key()

    # Novo usuário solicita chaves públicas dos usuários existentes
    request_keys_message = {
        "ip": local_ip,
        "type": "request_public_keys"
    }
    send_sock.sendto(json.dumps(request_keys_message).encode(), (multicast_group, port))

    while True:
        clear_screen()
        print("-----Bem vindo ao chat-----")
        print("[1] - Entrar no chat")
        print("[2] - Sair")

        choice = input("Escolha uma opção: ")

        if choice == '1':
            clear_screen()

            # Passe o vetor de relógio como argumento para o listener_thread
            listener_thread = threading.Thread(target=listen_for_messages, args=(vclock,), daemon=True)
            listener_thread.start()

            # Envie o histórico de mensagens para o novo usuário
            send_chat_history(get_local_ip_address())

            # Passe o vetor de relógio como argumento para send_message
            send_message(vclock)
        elif choice == '2':
            break

if __name__ == "__main__":
    main_menu()