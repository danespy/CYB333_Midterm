# Importing module to enable socket programming
import socket

# Define server host and port to listen on
HOST = '127.0.0.1' 
PORT = 65432

# Using IPv4 and TCP to create socket object
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"[+] Server listening on {HOST}:{PORT}...")

    conn, addr = s.accept()
    with conn:
        print(f"[+] Connected by {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            print("[Client]:", data,decode())
            conn.sendall(b"Message received!")