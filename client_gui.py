
import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

HOST = '127.0.0.1'
PORT = 65432

class ChatClient:
    def __init__(self, master):
        self.master = master
        self.master.title("Socket Chat Client")
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.chat_area = scrolledtext.ScrolledText(master, wrap=tk.WORD, state='disabled', width=60, height=20)
        self.chat_area.pack(padx=10, pady=10)

        self.msg_entry = tk.Entry(master, width=50)
        self.msg_entry.pack(side=tk.LEFT, padx=(10, 0), pady=(0, 10), expand=True, fill=tk.X)
        self.msg_entry.bind("<Return>", self.send_message)

        self.send_btn = tk.Button(master, text="Send", command=self.send_message)
        self.send_btn.pack(side=tk.RIGHT, padx=(0, 10), pady=(0, 10))

        self.connect_to_server()
        threading.Thread(target=self.receive_messages, daemon=True).start()

    def connect_to_server(self):
        try:
            self.sock.connect((HOST, PORT))
            self.display_message("[CLIENT] Connected to server.")
        except Exception as e:
            self.display_message(f"[ERROR] Could not connect: {e}")

    def send_message(self, event=None):
        msg = self.msg_entry.get()
        if msg:
            try:
                self.sock.sendall(msg.encode())
                self.msg_entry.delete(0, tk.END)
            except:
                self.display_message("[ERROR] Message could not be sent.")

    def receive_messages(self):
        while True:
            try:
                data = self.sock.recv(1024)
                if not data:
                    self.display_message("[INFO] Server disconnected.")
                    break
                self.display_message(data.decode())
            except:
                break

    def display_message(self, message):
        self.chat_area.config(state='normal')
        self.chat_area.insert(tk.END, message + '\n')
        self.chat_area.yview(tk.END)
        self.chat_area.config(state='disabled')

if __name__ == "__main__":
    root = tk.Tk()
    client = ChatClient(root)
    root.mainloop()
