import sys
import time
import socket
import threading

n = 0

def test():

    while True:
        global n
        time.sleep(1)
        print(f"{n} requests per second")
        n = 0


def throughput(port: int):
    with socket.socket() as sock:
        sock.connect(('', port))
        while True:
            sock.send(b'1')
            sock.recv(100)
            global n
            n += 1

if __name__ == "__main__":
    port = int(sys.argv[1])
    t = threading.Thread(target=throughput, args=(port,))
    u = threading.Thread(target=test, args=())
    t.start()
    u.start()


