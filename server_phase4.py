import socket
import threading
import time

HOST = '127.0.0.1'
PORT = 65432

clients = []
lock = threading.Lock()

def get_current_time():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

def broadcast(message, sender_conn, sender_addr):
    timestamp = get_current_time()
    tagged_message = f"[{timestamp}] [{sender_addr[0]}:{sender_addr[1]}] {message.decode()}"
    with lock:
        for conn in clients:
            if conn is not sender_conn:
                try:
                    conn.sendall(tagged_message.encode())
                except:
                    pass  # ignore broken connections

def send_private_message(target_ip, message, sender_addr):
    timestamp = get_current_time()
    pm = f"[{timestamp}] [Private from {sender_addr[0]}:{sender_addr[1]}] {message}"
    with lock:
        for conn in clients:
            if conn.getpeername()[0] == target_ip:
                try:
                    conn.sendall(pm.encode())
                except:
                    pass
                break

def list_clients(conn):
    with lock:
        user_list = "\n".join([f"{c.getpeername()[0]}:{c.getpeername()[1]}" for c in clients])
        conn.sendall(f"Connected users:\n{user_list}".encode())

def handle_client(conn, addr):
    print(f"[SERVER] {addr} connected")
    with lock:
        clients.append(conn)

    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break

            message = data.decode().strip()
            print(f"[SERVER] From {addr}: {message}")

            if message.startswith("<pm "):
                try:
                    parts = message.split(" ", 2)
                    target_ip = parts[1]
                    private_msg = parts[2]
                    send_private_message(target_ip, private_msg, addr)
                except:
                    conn.sendall("Invalid PM command. Use: <pm IP message>".encode())
            elif message == "<list>":
                list_clients(conn)
            else:
                broadcast(data, conn, addr)
    finally:
        with lock:
            clients.remove(conn)
        conn.close()
        print(f"[SERVER] {addr} disconnected")

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"[SERVER] Listening on {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
            thread.start()

if __name__ == "__main__":
    start_server()
