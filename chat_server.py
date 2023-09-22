import socket
import select
from threading import Thread
import argparse


def parse_args():
    parser = argparse.ArgumentParser(description="Chat server")
    parser.add_argument('ip', type=str, help="IP address of the machine hosting the server")
    parser.add_argument('--port', type=int, default=5000, help="Port number to listen on (default: 5000)")
    return parser.parse_args()


args = parse_args()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

IP_address = args.ip
Port = args.port

server.bind((IP_address, Port))
print("Chat Server started on " + IP_address + ":" + str(Port))
server.listen(100) # 100 is the maximum number of connections
list_of_clients = []


def client_thread(conn, addr):
    conn.send("Welcome to this chatroom!".encode())
    while True:
        try:
            message = conn.recv(2048)
            if message:
                print("<" + addr[0] + "> " + message.decode())  # Decode received message
                message_to_send = "<" + addr[0] + "> " + message.decode()  # Decode message to send
                broadcast(message_to_send.encode(), conn)  # Encode message before sending
            else:
                remove(conn)
        except:
            continue


def broadcast(message, connection):
    for clients in list_of_clients:
        if clients != connection:
            try:
                clients.send(message)
            except:
                clients.close()
                remove(clients)


def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)


while True:
    conn, addr = server.accept()
    list_of_clients.append(conn)
    print(addr[0] + " connected")
    Thread(target=client_thread, args=(conn, addr)).start()

conn.close()
server.close()
