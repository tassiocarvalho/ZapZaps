import socket
import threading
import sys
import json
from vetorclock import VetorClock

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

def receive_messages(sock, vetor_clock):
    global message_list, members
    while True:
        try:
            data, addr = sock.recvfrom(1024)
            if not data:
                continue

            message_data = json.loads(data.decode())

            if message_data['type'] == 'update_member_list':
                # Atualize a lista de membros local
                updated_members = set(tuple(m) for m in message_data['members'])
                members = updated_members
            elif message_data['type'] == 'new_member':
                # Mensagem para notificar a adição de um novo membro
                # (pode ser removida se desejar, já que a lista é atualizada acima)
                pass
            else:
                # Mensagens regulares
                message = f"{addr[0]} falou: {message_data['message']}"
                remote_clock = message_data['clock']
                for member, timestamp in remote_clock.items():
                    vetor_clock.update(member, timestamp)
                message_list.append(message)
                print_message_list()
        except Exception as e:
            print(f"Erro ao receber a mensagem: {e}")
            return

def print_message_list():
    global message_list
    print("\n(----------------------Mensagens---------------------)")
    for message in message_list:
        print(message)
    print("(----------------------------------------------------)\n")
    print("obs: Para adicionar um novo membro no grupo digite: /add_membro <IP> <PORTA>\n")
    print("Escreva sua mensagem: ", end="")
    
def add_member(ip, port, sock, vetor_clock):
    global members
    new_member = (ip, port)

    # Atualize a lista de membros
    members.add(new_member)

    # Enviar a lista atualizada de membros para todos os membros
    updated_members_data = json.dumps({
        'type': 'update_member_list',
        'members': list(members)
    }).encode()

    for member in members:
        try:
            sock.sendto(updated_members_data, member)
        except:
            print(f"Erro ao enviar a lista de membros atualizada para {member[0]}:{member[1]}")

    print(f"Membro {ip}:{port} adicionado com sucesso.")

def main():
    global message_list, members
    local_ip = get_local_ip_address()
    print("Seu IP é: " + local_ip)
    port = int(input("Digite a porta para usar no chat: "))
    members.add((local_ip, port))

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((local_ip, port))

    vetor_clock = VetorClock()  # Instância do VetorClock

    threading.Thread(target=receive_messages, args=(sock, vetor_clock), daemon=True).start()

    print_message_list()
    while True:
        message = input()

        if message.startswith("/add_membro"):
            _, member_ip, member_port = message.split()
            add_member(member_ip, int(member_port), sock, vetor_clock)  # Aqui também
            continue

        # Incrementa o vetor de relógio para a mensagem atual
        vetor_clock.increment((local_ip, port))

        # Prepara a mensagem com o vetor de relógio
        message_data = json.dumps({
            'type': 'message', 
            'message': message, 
            'clock': vetor_clock.get_clock()
        }).encode()

        message_list.append(f"Você: {message}")
        print_message_list()

        # Envio da mensagem para todos os membros
        for member in members:
            if member != (local_ip, port):
                try:
                    sock.sendto(message_data, member)
                except:
                    print(f"Erro ao enviar mensagem para {member[0]}:{member[1]}")

if __name__ == "__main__":
    main()