# Import socket module for client
import socket

# Define the server host and port to connect to
HOST = '127.0.0.1'  
PORT = 65432    

# Create socket object with IPv4 and TCP protocol
try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Connect to the server
        s.connect((HOST, PORT))
        print(f"[+] Connected to server at {HOST}:{PORT}")

        # Send a message to the server
        message = "Hello, Server!"
        s.sendall(message.encode())
        print("[Client]:", message)

        # Receive response from the server
        data = s.recv(1024)
        print("[Server]:", data.decode())

except ConnectionRefusedError:
    print("[-] Connection failed. Is the server running?")