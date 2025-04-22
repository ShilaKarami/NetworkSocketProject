import socket
import threading
import sys

HOST = '127.0.0.1'
PORT = 65432

def receive_messages(sock):
    while True:
        data = sock.recv(1024)
        if not data:
            print("[CLIENT] Disconnected from server")
            sys.exit()
        print(f"[MSG] {data.decode().strip()}")

def start_client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_sock:
        client_sock.connect((HOST, PORT))
        print("[CLIENT] Connected! Type messages and press Enter to send.")
        
        # Start thread to listen for broadcasts
        threading.Thread(target=receive_messages, args=(client_sock,), daemon=True).start()

        # Main thread: send user input
        while True:
            msg = input()
            if msg.lower() == "exit":
                break
            client_sock.sendall(msg.encode())

if __name__ == "__main__":
    start_client()
