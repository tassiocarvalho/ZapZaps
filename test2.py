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
    global message_list, members
    while True:
        try:
            data, addr = sock.recvfrom(1024)
            if data.decode().startswith("/novo_membro"):
                _, new_ip, new_port = data.decode().split()
                members.add((new_ip, int(new_port)))
                message = f"Novo membro adicionado: {new_ip}:{new_port}"
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
    print("(----------------------------------------------------)\n")
    print("obs: Para adicionar um novo membro no grupo digite: /add_membro <IP> <PORTA>\n")
    print("Escreva sua mensagem: ", end="")

def add_member(ip, port, sock):
    global members
    new_member = (ip, port)
    members.add(new_member)

    # Informa o novo membro sobre todos os membros existentes
    for member in members:
        if member != new_member:
            try:
                sock.sendto(f"/novo_membro {member[0]} {member[1]}".encode(), new_member)
            except:
                print(f"Erro ao informar o novo membro {new_member[0]}:{new_member[1]} sobre o membro existente {member[0]}:{member[1]}")

    # Informa os outros membros sobre o novo membro
    for member in members:
        if member != new_member:
            try:
                sock.sendto(f"/novo_membro {ip} {port}".encode(), member)
            except:
                print(f"Erro ao informar {member[0]}:{member[1]} sobre o novo membro")

    print(f"Membro {ip}:{port} adicionado com sucesso.")

def main():
    global message_list, members
    local_ip = get_local_ip_address()
    print("Seu IP é: " + local_ip)
    port = int(input("Digite a porta para usar no chat: "))
    members.add((local_ip, port))

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((local_ip, port))

    threading.Thread(target=receive_messages, args=(sock,), daemon=True).start()

    print_message_list()
    while True:
        message = input()

        if message.startswith("/add_membro"):
            _, member_ip, member_port = message.split()
            add_member(member_ip, int(member_port), sock)
            continue

        message_list.append(f"Você: {message}")
        print_message_list()

        for member in members:
            if member != (local_ip, port):
                try:
                    sock.sendto(message.encode(), member)
                except:
                    print(f"Erro ao enviar mensagem para {member[0]}:{member[1]}")

if __name__ == "__main__":
    main()