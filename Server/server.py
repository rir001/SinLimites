from pickle import dumps, loads
from threading import Thread
import numpy as np
import cv2

class Servidor:

    def __init__(self, socket) -> None:
        self.socket = socket
        self.socket.listen(1)
        self.clients = []

    def start(self):
        self.run = True
        self.start_listen()

    def start_listen(self):
        Thread(target=self.listen, daemon=True).start()

    def listen(self):
        while self.run:
            try:
                client_socket, ip = self.socket.accept()
                print(f'Conexion detectada desde {ip[0]}')
                self.recv_client_loop(client_socket)

            except Exception as e:
                print('( ! ) Se detecto un intento de conexion pero ocurrio un error:\n', e)


    def recv_client_loop(self, client_socket):
        self.clients.append(client_socket)
        Thread(target=self.recv_client,  kwargs={"id":self.clients.index(client_socket)}, daemon=True).start()



    def recv_client(self, id):
        try:
            while self.run:
                message = self.clients[id].recv(1024*500)
                if not message:
                    raise ConnectionResetError
                print(len(message))
                self.process_message(message, id)


        except (ConnectionError, ConnectionResetError) as error:
            print(f'( ! ) Se ha perdido la conexion con el cliente {id}: ', error)


    def process_message(self, message, id):
        message = loads(message)
        if message["TIPE"] == "MESSAGE":
            print(message["VALUE"])
        elif message["TIPE"] == "IMAGE":


            image = np.frombuffer(message["VALUE"], dtype=np.uint8)
            image = cv2.imdecode(image, flags=1)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image = cv2.imencode('.png', image)[1]
            image = np.array(image).tobytes()

            self.send("IMAGE", image, id)

        else:
            print(message)



    def send(self, tipe, data, id):
        message = dumps({"TIPE":tipe, "VALUE":data})
        self.clients[id].send(message)