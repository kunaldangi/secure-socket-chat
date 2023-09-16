import socket
import threading

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('0.0.0.0', 12345)
server_socket.bind(server_address)

server_socket.listen(5) # Listen for incoming connections (max 5 clients in the queue)
print("Server is listening for incoming connections...")

all_clients = []

def handle_client(client_socket, client_address):
    while True:
        data = client_socket.recv(1024) # Receive data from the client
        if not data:
            break  # Client disconnected
        print(f"{client_address}: {data.decode()}")

        
        response = "Status:200"
        client_socket.send(response.encode()) # Send a response back to the client

        for x in all_clients:
            if x[0] != client_socket:
                x[0].send(f"{x[1]}: {data.decode()}".encode())
        
    for x in all_clients:
        if x[0] == client_socket:
            all_clients.remove(x)

    client_socket.close() # Close the client socket


while True:
    print("Waiting for a connection...")
    client_socket, client_address = server_socket.accept() # Wait for a connection
    print(f"Connection established with {client_address}")

    all_clients.append([client_socket, client_address])

    client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address)) # Create a new thread to handle the client
    client_thread.start()
