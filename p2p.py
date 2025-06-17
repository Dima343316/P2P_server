import socket
import threading

from crypto import encrypt_message, decrypt_message


class P2PNode:
    def __init__(self, host, port):
        self.host = host  # IP-адрес
        self.port = port # Порт
        self.peers = set()  #Сокеты
        self.lock = threading.Lock()

    def start(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # 💡 Это обязательно!
        server.bind((self.host, self.port))
        server.listen()
        print(f"[P2P] Listening on {self.host}:{self.port}")

        while True:
            conn, addr = server.accept() #принятие
            print(f"[P2P] Connected by {addr}")
            with self.lock:
                self.peers.add(conn)  # добавлнение пира
            threading.Thread(target=self.handle_peer,
                             args=(conn, addr),
                             daemon=True
                             ).start()

    def handle_peer(self, conn, addr):
        try:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                try:
                    decrypted = decrypt_message(data)
                    print(f"[P2P] Received from {addr}: {decrypted}")
                except Exception as e:
                    print(f"[P2P] Error decrypting message from {addr}: {e}")
        finally:
            with self.lock:
                self.peers.discard(conn)
            conn.close()
            print(f"[P2P] Connection with {addr} closed")

    def connect_to_peer(self, host, port):
        try:
            conn = socket.create_connection((host, port))
            with self.lock:
                self.peers.add(conn)
            threading.Thread(target=self.handle_peer, args=(conn, (host, port)), daemon=True).start()
            print(f"[P2P] Connected to {host}:{port}")
        except Exception as e:
            print(f"[P2P] Could not connect to {host}:{port} - {e}")

    def broadcast(self, message):
        encrypted = encrypt_message(message)
        print(f"[P2P] Broadcasting: {message}")  # <== это лог для понимания, вызывается ли вообще
        with self.lock:
            for peer in list(self.peers):
                try:
                    print(f"[P2P] Sending to {peer.getpeername()}")  # <== чтобы понять, куда именно
                    peer.sendall(encrypted)
                except Exception as e:
                    print(f"[P2P] Failed to send: {e}")
                    self.peers.discard(peer)

__all__=()
