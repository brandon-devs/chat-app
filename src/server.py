import socket
import threading

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

conns = []

def send(uname, msg, conn):

    username = uname.encode(FORMAT)
    uname_len = len(username)
    uname_send_len = str(uname_len).encode(FORMAT)
    uname_send_len += b' ' * (HEADER - len(uname_send_len))
    conn.send(uname_send_len)
    conn.send(username)

    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    conn.send(send_length)
    conn.send(message)

def handle_client(conn, addr):

    conns.append(conn)

    username_length = conn.recv(HEADER).decode(FORMAT)
    if username_length:
        username_length = int(username_length)
        username = conn.recv(username_length).decode(FORMAT)

    print(f"[NEW CONNECTION... {username}]")

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                print(f"{username} has disonnected")
                connected = False
            else:
                for client in conns:
                    send(username, msg, client)
                print(f"[{username}] {msg}")
    
    conn.close()

def start():
    server.listen()
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

print("[STARTING SERVER...]")
start()
