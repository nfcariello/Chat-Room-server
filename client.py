import socket
import select
import sys
import argparse


def parse_args():
    parser = argparse.ArgumentParser(description="Chat client")
    parser.add_argument('ip', type=str, help="IP address of the server")
    parser.add_argument('--port', type=int, default=5000, help="Port number of the server (default: 5000)")
    return parser.parse_args()


args = parse_args()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

IP_address = args.ip
Port = args.port

try:
    server.connect((IP_address, Port))
except:
    print("Connection refused")
    sys.exit()

while True:
    sockets_list = [sys.stdin, server]
    read_sockets, write_socket, error_socket = select.select(sockets_list, [], [])
    for socks in read_sockets:
        if socks == server:
            message = socks.recv(2048)
            print(message.decode())
        else:
            message = input()
            server.send(message.encode())
            sys.stdout.write("<You> ")
            sys.stdout.write(message)
            sys.stdout.write("\n")
            sys.stdout.flush()

server.close()