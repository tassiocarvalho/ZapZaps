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

def receive_messages(sock, local_ip, local_port):
    global message_list, members
    while True:
        try:
            data, addr = sock.recvfrom(1024)  # Buffer size 1024 bytes
            if addr[0] == local_ip and addr[1] == local_port:
                continue  # Ignora mensagens enviadas pelo próprio usuário

            if data.decode().startswith("/new_member_list"):
                # Atualiza a lista de membros
                new_members = json.loads(data.decode().split(" ", 1)[1])
                members.update(new_members)
                print_message_list()
            else:
                message = f"{addr[0]} falou: {data.decode()}"
                message_list.append(message)
                print_message_list()
        except:
            print("Erro ao receber a mensagem.")
            return

def print_message_list():
    global message_list
    print("\n(----------------------Mensagens---------------------)")
    for message in message_list:
        print(message)
    print("(----------------------------------------------------)")
    print("Escreva sua mensagem: ", end="")

def add_member(ip, port, sock):
    global members
    new_member = (ip, port)
    members.add(new_member)
    print(f"Membro {ip}:{port} adicionado com sucesso.")
    # Envia a lista de membros atualizada para todos os membros, incluindo o novo membro
    member_list_message = "/new_member_list " + json.dumps(list(members))
    for member in members:
        sock.sendto(member_list_message.encode(), member)

def main():
    global message_list, members
    local_ip = get_local_ip_address()
    print("Seu ip é: "+ local_ip)
    port = int(input("Digite a porta para usar no chat: "))

    # Configuração do socket UDP
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((local_ip, port))

    # Iniciando thread para receber mensagens
    threading.Thread(target=receive_messages, args=(sock, local_ip, port), daemon=True).start()

    print_message_list()
    while True:
        message = input()

        if message.startswith("/add_membro"):
            _, member_ip, member_port = message.split()
            add_member(member_ip, int(member_port), sock)
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