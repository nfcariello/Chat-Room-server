import os
import socket
import select
from threading import Thread
import argparse
import datetime


def create_logs_folder():
    if not os.path.exists("logs"):
        os.mkdir("logs")


def parse_args():
    parser = argparse.ArgumentParser(description="Chat server")
    parser.add_argument('ip', type=str, help="IP address of the machine hosting the server")
    parser.add_argument('--port', type=int, default=5000, help="Port number to listen on (default: 5000)")
    return parser.parse_args()


create_logs_folder()  # Create the "logs" folder if it doesn't exist

args = parse_args()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

IP_address = args.ip
Port = args.port

server.bind((IP_address, Port))
print("Chat Server started on " + IP_address + ":" + str(Port))
server.listen(100)
list_of_clients = []

# Generate a timestamp for the log file name
timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_file_name = os.path.join("logs", f"chat_log_{timestamp}.txt")  # Use os.path.join to specify the folder

# Open a new log file for writing
log_file = open(log_file_name, "a")


def log_entry(message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"{timestamp} {message}\n"
    print(log_message)
    log_file.write(log_message)
    log_file.flush()


def client_thread(conn, addr):
    name = conn.recv(2048).decode()
    log_entry(f"User '{name}' joined from {addr[0]}")
    welcome_message = f"Welcome to this chatroom, {name}!"
    conn.send(welcome_message.encode())
    while True:
        try:
            message = conn.recv(2048)
            if message:
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                log_message = f"{timestamp} <{name}> {message.decode()}\n"
                print(log_message)
                log_file.write(log_message)
                log_file.flush()
                message_to_send = "<" + name + "> " + message.decode()
                broadcast(message_to_send.encode(), conn)
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
