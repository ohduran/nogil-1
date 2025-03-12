from typing import List
import threading
import socket
import sys


def load_balancer(port:int, SERVER_CONNECTIONS: LeastConnectionRouter): 
    with socket.socket() as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('', port))
        sock.listen(5)

        while True:
            try:
                conn, addr = sock.accept()
                print(f"Load balancer accepting connections on {addr}")

                server_port = SERVER_CONNECTIONS.get_port()
                t = threading.Thread(target=balancing, name=addr, args=(conn, server_port, addr, SERVER_CONNECTIONS))
                t.start()
            except Exception as e:
                print(f"Load balancer error: {e}")
            
def balancing(conn: socket.socket, server_port: int, addr: str, SERVER_CONNECTIONS: LeastConnectionRouter):
    with socket.socket() as server_socket:
        print(f"The load balancer is routing to server on port {server_port}")
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.connect(('localhost', server_port))
        while True:
            data = conn.recv(1024)
            print(f"Data received from {addr}: {data.decode()}")
            if not data:
                print(f"Connection closed by {addr}")
                break

            server_socket.sendall(data)
            response = server_socket.recv(1024)
            print(f"Data sent from server: {response.decode()}")
            if not response:
                print(f"Connection closed by server {server_port}")
                break
                
            conn.sendall(response)
    SERVER_CONNECTIONS.decrement(server_port)



def lb_algo(server_ports: List[int]) -> int:
    # Random round robin for now
    from random import choice
    return choice(server_ports)


class LeastConnectionRouter:

    def __init__(self, server_ports: List[int]):
        self.server_connections = {port: 0 for port in server_ports}
        self._lock = threading.Lock()

    def _increment(self, port: int):
        self.server_connections[port] += 1
        print(self, 1)

    def decrement(self, port: int):
        with self._lock:
            self.server_connections[port] -= 1
            print(self, -1)

    def get_port(self) -> int:
        with self._lock:
            server_port = min(self.server_connections.keys(), key=lambda x: self.server_connections[x])
            self._increment(server_port)
        return server_port
    
    def __repr__(self):
        return str({key: value for key, value in self.server_connections.items()})



if __name__ == "__main__":
   lb_port = sys.argv[1]
   server_ports = sys.argv[2:]

   SERVER_CONNECTIONS = LeastConnectionRouter(list(map(int, server_ports)))

   load_balancer(int(lb_port), SERVER_CONNECTIONS)


