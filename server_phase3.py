import socket
import threading

HOST = '127.0.0.1'
PORT = 65432

# Keep track of all connected clients
clients = []

lock = threading.Lock()

def broadcast(message, sender_conn, sender_addr):
    """Send message to all clients except the sender, and include the sender's IP."""
    # Prepend sender's IP to the message
    tagged_message = f"[{sender_addr[0]}:{sender_addr[1]}] {message.decode()}"
    with lock:
        for conn in clients:
            if conn is not sender_conn:
                try:
                    conn.sendall(tagged_message.encode())
                except:
                    # In case connection is broken, ignore the error
                    pass

def handle_client(conn, addr):
    print(f"[SERVER] {addr} connected")
    with lock:
        clients.append(conn)

    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break  # client disconnected
            print(f"[SERVER] From {addr}: {data.decode().strip()}")
            # broadcast to others
            broadcast(data, conn, addr)
    finally:
        with lock:
            clients.remove(conn)
        conn.close()
        print(f"[SERVER] {addr} disconnected")

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_sock:
        server_sock.bind((HOST, PORT))
        server_sock.listen()
        print(f"[SERVER] Listening on {HOST}:{PORT}")

        while True:
            conn, addr = server_sock.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
            thread.start()

if __name__ == "__main__":
    start_server()
