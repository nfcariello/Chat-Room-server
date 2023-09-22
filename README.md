# Chat-Room-server

# Start A Chat Server
1. Start the server by running the following command in the terminal:
```
python3 chat_server.py <ip_address> --port <port_number>
```
You will need to pass the IP address of the machine hosting the server, and (optionally) the port number you want to host on. If no port number is passed, the default port number is 5000.

# Start a Terminal Client Connection
1. Start a client connection by running the following command in the terminal:
```
python3 client.py <ip_address> --port <port_number>
```
You will need to pass the IP address and (optionally) the port number of the server you want to connect to. If no port number is passed, the default port number is 5000.

# Start a GUI Client Connnection
1. Start a client connection by running the following command in the terminal:
```
python3 gui_client.py
```
You will be prompted for the IP address and port number of the server you want to connect to. If no port number is provided, the default port number is 5000.
You'll also need to provide your name for joining the chat.