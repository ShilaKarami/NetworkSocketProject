import socket
import threading
import time

HOST = '127.0.0.1'
PORT = 65432

def handle_client(conn, addr):
    print(f"[SERVER] New connection from {addr}")
    try:
        data = conn.recv(1024).decode()
        if data:
            print(f"[SERVER] Received from {addr}: {data}")
            conn.sendall("Hello Client!".encode())

        # ← HOLD THE CONNECTION OPEN FOR 10s SO YOU CAN SEE THEM ALL
        print(f"[SERVER] Keeping connection with {addr} open for 10s")
        time.sleep(10)

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
            thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
            thread.start()
            # subtract 1 for the main thread
            print(f"[SERVER] Active Connections: {threading.active_count() - 1}")

if __name__ == "__main__":
    start_server()
