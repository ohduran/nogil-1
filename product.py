import threading
import sys
from load_balancer import load_balancer, LeastConnectionRouter
from server import server

if __name__ == "__main__":
   lb_port = sys.argv[1]
   server_ports = sys.argv[2:]

   SERVER_CONNECTIONS = LeastConnectionRouter(list(map(int, server_ports)))

   for server_port in server_ports:
       threading.Thread(target=server, args=(int(server_port),)).start()

   load_balancer(int(lb_port), SERVER_CONNECTIONS)



