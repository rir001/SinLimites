from server import Servidor
import socket
import sys


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    sock.bind(('192.168.0.15', 5010))
    print("El servidor está en linea")
    serv = Servidor(sock)

except socket.error:
    print("No se pudo iniciar el servidor")
    sys.exit()

serv.start()

if input() != None:
    sys.exit()