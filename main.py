import threading
import time
from p2p import P2PNode
from http_api import start_http_server

if __name__ == "__main__":
    node = P2PNode(host='127.0.0.1', port=7000)
    threading.Thread(target=node.start, daemon=True).start()
    threading.Thread(target=start_http_server, args=(node, 8001), daemon=True).start()

    while True:
        node.broadcast("Hello, NET!")
        time.sleep(5)
