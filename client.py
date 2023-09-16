import socket
import threading

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a socket object
server_address = ('localhost', 12345) # Define the server address and port
client_socket.connect(server_address) # Connect to the server


def send_message(client_socket):
    while True:
        message = str(input("Enter the message: "))
        client_socket.send(message.encode())

def recieve_message(client_socket):
    while True:
        response = client_socket.recv(1024) # Receive a response from the server
        print(f"Server: {response.decode()}")


send_thread = threading.Thread(target=send_message, args=(client_socket, )) # Create a new thread to handle the client
send_thread.start()
recieve_thread = threading.Thread(target=recieve_message, args=(client_socket, )) # Create a new thread to handle the client
recieve_thread.start()

# client_socket.close() # Close the client socket