import socket
import time

HOST = '127.0.0.1'
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((HOST, PORT))
    message = "Hello Server!"
    client_socket.sendall(message.encode())
    print(f"[CLIENT] Sent: {message}")
    
    data = client_socket.recv(1024).decode()
    print(f"[CLIENT] Received: {data}")

    print("[CLIENT] Keeping the connection open for 10 seconds...")
    time.sleep(10)  # Keep it open for 10 seconds to see active connections
