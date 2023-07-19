from client import Cliente
import socket
import sys


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    sock.connect(("190.46.22.184", 5010))
    print("Conexion exitosa")
    cli = Cliente(sock)

except socket.error:
    print("La conexion falló")
    sys.exit()

cli.start()

sys.exit()