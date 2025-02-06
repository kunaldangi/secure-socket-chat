import socket
import threading

port = 4444
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('0.0.0.0', port)
server_socket.bind(server_address)

server_socket.listen(5) # Listen for incoming connections (max 5 clients in the queue)
print(f"Server is listening on PORT: {port}")
print("Server is listening for incoming connections...")

all_clients = []

def getIpPort(client_address):
    return f"{client_address[0]}:{client_address[1]}"

def handle_client(client_socket, client_address):
    while True:
        try:
            data = client_socket.recv(1024) # Receive data from the client
            if not data:
                break
            print(f"{getIpPort(client_address)}: {data.decode()}")
        except ConnectionResetError:
            print(f"{getIpPort(client_address)} disconnected")

            for x in all_clients:
                if x[0] != client_socket:
                    x[0].send(f"{getIpPort(client_address)} disconnected".encode())

                if x[0] == client_socket:
                    all_clients.remove(x)
            break

        
        response = "Status:200"
        client_socket.send(response.encode()) # Send a response back to the client

        for x in all_clients:
            if x[0] != client_socket:
                x[0].send(f"{getIpPort(client_address)}: {data.decode()}".encode())
        
    for x in all_clients:
        if x[0] == client_socket:
            all_clients.remove(x)

    client_socket.close() # Close the client socket


while True:
    print("Waiting for a connection...")
    client_socket, client_address = server_socket.accept() # Wait for a connection
    print(f"Connection established with {getIpPort(client_address)}")
    client_socket.send("Connection established".encode())
    for x in all_clients:
        x[0].send(f"{getIpPort(client_address)} connected".encode())

    all_clients.append([client_socket, client_address])

    client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address)) # Create a new thread to handle the client
    client_thread.start()
