import socket
import threading
import sys

clientes = []  # Lista para manter o rastreamento dos clientes

def receive_messages(sock):
    while True:
        try:
            message, address = sock.recvfrom(1024)
            print(f"\nMensagem de {address}: {message.decode()}\nDigite sua mensagem: ", end="")

            # Adicionando o cliente à lista, se ainda não estiver nela
            if address not in clientes:
                clientes.append(address)

            # Retransmitindo a mensagem para todos os clientes, exceto para o remetente
            for client in clientes:
                if client != address:
                    sock.sendto(f"Mensagem de {address}: {message.decode()}".encode(), client)

        except Exception as e:
            print(f"Erro ao receber mensagem: {e}")
            break

def send_messages(sock, target_ip, target_port):
    while True:
        message = input("\nDigite sua mensagem (digite 'sair' para finalizar): ")
        if message == 'sair':
            break
        sock.sendto(message.encode(), (target_ip, target_port))

def start_server(port):
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind(('', port))
    print(f"Servidor iniciado na porta {port}. Você também pode enviar mensagens.")

    threading.Thread(target=receive_messages, args=(server,), daemon=True).start()

    # Loop para enviar mensagens no modo servidor
    send_messages(server, 'localhost', port)

def start_client(server_ip, server_port):
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print(f"Cliente conectado ao servidor {server_ip} na porta {server_port}.")

    send_messages(client, server_ip, server_port)

def main():
    port = int(input("Digite a porta para usar (sugestão: entre 5000 e 65535): "))
    choice = input("Escolha uma opção:\n[1] Aguardar conexão no chat\n[2] Adicionar um peer para conectar no chat\n")

    if choice == '1':
        start_server(port)
    elif choice == '2':
        peer_ip = input("Digite o IP do peer: ")
        peer_port = int(input("Digite a porta do peer: "))
        start_client(peer_ip, peer_port)
    else:
        print("Opção inválida.")
        sys.exit()

if __name__ == "__main__":
    main()
