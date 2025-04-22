import socket

HOST = '127.0.0.1'  # localhost
PORT = 65432        # Non-privileged port

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"[SERVER] Listening on {HOST}:{PORT}")
    
    conn, addr = server_socket.accept()
    with conn:
        print(f"[SERVER] Connected by {addr}")
        data = conn.recv(1024).decode()
        print(f"[SERVER] Received: {data}")
        if data:
            response = "Hello Client!"
            conn.sendall(response.encode())
        print("[SERVER] Connection closed")
