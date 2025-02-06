import socket
import threading
import tkinter as tk
import ssl
# import tkinter.ttk as ttk

client_socket = None
server_address = None
canvas = None
scrollbar = None
frame1 = None

window = tk.Tk()
window.geometry("600x400")

context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE  # Disable verification for local testing

def recieve_message():
    global client_socket
    while True:
        try:
            response = client_socket.recv(1024) # Receive a response from the server
            if not response:
                break  # Connection closed

            print(f"Server: {response.decode()}")
            if "Status:200" != response.decode():
                greeting = tk.Label(frame1, text=f"{response.decode()}")
                greeting.pack()

                frame1.update_idletasks()
                canvas.config(scrollregion=canvas.bbox("all"))
                canvas.yview_moveto(1.0)

        except (ConnectionResetError, OSError):
            print("Connection lost.")
            break


def connect_to_server(connect_input, port_input, filewin):
    global client_socket
    try:
        raw_socket = socket.create_connection((connect_input.get(), int(port_input.get())))
        client_socket = context.wrap_socket(raw_socket, server_hostname=connect_input.get())


        # send_thread = threading.Thread(target=send_message, args=(client_socket, )) # Create a new thread to handle the client
        # send_thread.start()
        receive_thread = threading.Thread(target=recieve_message, daemon=True) # Create a new thread to handle the client
        receive_thread.start()

        filewin.destroy()

    except Exception as e:
        print(f"Connection failed: {e}")

def connect_page():
    filewin = tk.Toplevel(window)
    filewin.geometry("300x150")

    connect_text = tk.Label(filewin, text="IP Address:")
    connect_text.pack()
    connect_input = tk.Entry(filewin)
    connect_input.pack()

    port_text = tk.Label(filewin, text="Port:")
    port_text.pack()
    port_input = tk.Entry(filewin)
    port_input.pack()

    connect_btn = tk.Button(filewin, text="Connect", command=lambda: connect_to_server(connect_input, port_input, filewin))
    connect_btn.pack()


def disconnect():
    global client_socket
    if client_socket:
        try:
            client_socket.close()
            print("Disconnected.")
        except Exception as e:
            print(f"Error closing connection: {e}")
        client_socket = None

menubar = tk.Menu(window)
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label="Connect", command=connect_page)
filemenu.add_command(label="Disconnect", command=disconnect)
filemenu.add_command(label="Quit", command=window.quit)

menubar.add_cascade(label="Option", menu=filemenu)



canvas = tk.Canvas(window)
canvas.pack(fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(canvas)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

canvas.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=canvas.yview)

frame1 = tk.Frame(canvas)
canvas.create_window((0, 0), window=frame1, anchor=tk.NW)

frame1.update_idletasks()
canvas.config(scrollregion=canvas.bbox("all"))

frame2 = tk.Frame(window, background="blue")
frame2.pack(side=tk.BOTTOM, fill=tk.X, anchor=tk.W)

send_input = tk.Entry(frame2)
send_input.pack(fill=tk.X)

def send_message(send_input):
    global client_socket
    if client_socket:
        try:
            message = str(send_input.get())
            client_socket.send(message.encode())

            greeting = tk.Label(frame1, text=f"You: {message}")
            greeting.pack()

            frame1.update_idletasks()
            canvas.config(scrollregion=canvas.bbox("all"))
            canvas.yview_moveto(1.0)

        except (BrokenPipeError, OSError):
            print("Error: Connection lost while sending message.")

send_btn = tk.Button(send_input, text="Send", command=lambda ip=send_input: send_message(ip))
send_btn.pack(side=tk.RIGHT)

window.config(menu=menubar)
window.mainloop()
