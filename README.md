# Chat-Room-server

# Start A Chat Server
1. Start the server by running the following command in the terminal:
```
python3 chat_server.py
```
Optionally, you can pass in the port number and IP address as an argument. If no port number is passed, the default port number is 5000, and the default IP is the local IP of the machine.
```
python3 chat_server.py --ip <ip_address> --port <port_number>
```

# Start a Client Connection
1. Start a client connection by running the following command in the terminal:
```
python3 client.py <ip_address> --port <port_number>
```
You will need to pass the IP address and (optionally) the port number of the server you want to connect to. If no port number is passed, the default port number is 5000.