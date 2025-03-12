import sys
import time
import socket


def test(port: int):
    while True:
        with socket.socket() as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.connect(("localhost", port))
            start = time.time()
            sock.send(b"1")
            sock.recv(1012)
            end = time.time()

        print(f"{end - start}")

if __name__ == "__main__":
    test(int(sys.argv[1]))
