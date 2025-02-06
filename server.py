import socket
import threading
import ssl

port = 4444

# Load SSL context
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile="server-cert.pem", keyfile="server-key.key")

# Create and bind socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('0.0.0.0', port)
server_socket.bind(server_address)
server_socket.listen(5)

print(f"Server is listening on PORT: {port}")
print("Server is listening for incoming secure connections...")

all_clients = []


def getIpPort(client_address):
    return f"{client_address[0]}:{client_address[1]}"


def handle_client(secure_socket, client_address):
    while True:
        try:
            data = secure_socket.recv(1024)
            if not data:
                break
            print(f"{getIpPort(client_address)}: {data.decode()}")

            # Broadcast message to other clients
            for x in all_clients:
                if x[0] != secure_socket:
                    x[0].send(f"{getIpPort(client_address)}: {data.decode()}".encode())

        except ConnectionResetError:
            print(f"{getIpPort(client_address)} disconnected")

            # Notify other clients of disconnection
            for x in all_clients:
                if x[0] != secure_socket:
                    x[0].send(f"{getIpPort(client_address)} disconnected".encode())

            if [secure_socket, client_address] in all_clients:
                all_clients.remove([secure_socket, client_address])

            break

    if [secure_socket, client_address] in all_clients:
        all_clients.remove([secure_socket, client_address])

    secure_socket.close()


while True:
    print("Waiting for a secure connection...")
    client_socket, client_address = server_socket.accept()  # Accept a connection
    secure_socket = context.wrap_socket(client_socket, server_side=True)  # Secure the connection
    print(f"Secure connection established with {getIpPort(client_address)}")

    secure_socket.send("Secure connection established".encode())

    # Notify existing clients
    for x in all_clients:
        x[0].send(f"{getIpPort(client_address)} connected".encode())

    all_clients.append([secure_socket, client_address])

    client_thread = threading.Thread(target=handle_client, args=(secure_socket, client_address))
    client_thread.start()
