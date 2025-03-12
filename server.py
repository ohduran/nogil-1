import socket
from fib import fib
import threading
import sys

def server(port: int):
    with socket.socket() as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('', port))
        sock.listen(5)

        while True:
            conn, addr = sock.accept()
            t = threading.Thread(target=fibbing, args=(conn, addr))
            t.start()

    
def fibbing(conn: socket.socket, addr: str):
    print(f"Server established connection in {addr}")
    while True:
        data = conn.recv(1024)
        if not data: 
            print(f"Client closed connection in {addr}")
            break

        request = int(data.decode())
        response = str(fib(request)).encode() + b'\n'
        conn.sendall(response)



if __name__ == "__main__":
    port = sys.argv[1]
    server(int(port))

            

