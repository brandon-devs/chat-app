import socket
import threading

HEADER = 64
PORT = 5050
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = socket.gethostbyname(socket.gethostname())
ADDRESS = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDRESS)

print("JOINING SERVER...")

def send(msg):

    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)

def handle_messages(aClient):

    connected = True
    while connected:

        username_length = aClient.recv(HEADER).decode(FORMAT)
        if username_length:
            username_length = int(username_length)
            username = aClient.recv(username_length).decode(FORMAT)   

        msg_length = aClient.recv(HEADER).decode(FORMAT)
        if msg_length:

            msg_length = int(msg_length)
            msg = aClient.recv(msg_length).decode(FORMAT)

            if msg == DISCONNECT_MESSAGE:
                print(f"{username} has disonnected")
                connected = False
            else: 
                if username != username_input:
                    print(f"[{username}] {msg}")
