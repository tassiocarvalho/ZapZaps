import socket
import threading
import sys

message_list = []
members = set()

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

def receive_messages(sock):
    global message_list
    while True:
        try:
            data, addr = sock.recvfrom(1024)  # Buffer size 1024 bytes
            message = f"{addr[0]} falou: {data.decode()}"
            message_list.append(message)
            print_message_list()
        except:
            print("Erro ao receber a mensagem.")
            break

def print_message_list():
    global message_list
    print("\n(----------------------Mensagens---------------------)")
    for message in message_list:
        print(message)
    print("(----------------------------------------------------)")
    print("Escreva sua mensagem: ", end="")

def add_member(ip, port):
    global members
    members.add((ip, port))
    print(f"Membro {ip}:{port} adicionado com sucesso.")

def main():
    global message_list, members
    local_ip = get_local_ip_address()
    print("Seu ip é: "+ local_ip)
    port = int(input("Digite a porta para usar no chat: "))

    # Configuração do socket UDP
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((local_ip, port))

    # Iniciando thread para receber mensagens
    threading.Thread(target=receive_messages, args=(sock,), daemon=True).start()

    print_message_list()
    while True:
        message = input()

        if message.startswith("/add_membro"):
            _, member_ip, member_port = message.split()
            add_member(member_ip, int(member_port))
            print_message_list()
            continue

        message_list.append(f"Você: {message}")
        print_message_list()

        for member in members:
            try:
                sock.sendto(message.encode(), member)
            except:
                print(f"Erro ao enviar mensagem para {member[0]}:{member[1]}")

if __name__ == "__main__":
    main()