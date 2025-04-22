import socket
import threading

HOST = '127.0.0.1'
PORT = 65432

def handle_client(conn, addr):
    print(f"[SERVER] New connection from {addr}")
    try:
        data = conn.recv(1024).decode()
        if data:
            print(f"[SERVER] Received from {addr}: {data}")
            response = "Hello Client!"
            conn.sendall(response.encode())
    finally:
        print(f"[SERVER] Disconnected from {addr}")
        conn.close()

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print(f"[SERVER] Listening on {HOST}:{PORT}")

        while True:
            conn, addr = server_socket.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()
            print(f"[SERVER] Active Connections: {threading.active_count() - 1}")

if __name__ == "__main__":
    start_server()
