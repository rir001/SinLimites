from pickle import dumps, loads
from threading import Thread
from utils import get_int

class Cliente:

    def __init__(self, socket) -> None:
        self.socket = socket

    def start(self):
        Thread(target=self.recv_client, daemon=True).start()
        self.main()



    def main(self):
        run = True
        while run:
            print("""
[0] Salir
[1] Enviar mensaje
[2] Enviar imagen
""")
            option = get_int(0, 2)
            if option == 0:
                run = False
            elif option == 1:
                self.send("MESSAGE", input("Mensaje: "))
            elif option == 2:
                self.send("IMAGE", open("manzana.jpg", "rb").read())



    def recv_client(self):
        try:
            while True:
                message = self.socket.recv(1024*500)
                if not message:
                    raise ConnectionResetError
                print(len(message))
                self.process_message(message)

        except (ConnectionError, ConnectionResetError) as error:
            print(f'( ! ) Se ha perdido la conexion con el servidor: ', error)


    def process_message(self, message):
        message = loads(message)
        if message["TIPE"] == "MESSAGE":
            print("Mensaje recibido")
            print(message["VALUE"])
        elif message["TIPE"] == "IMAGE":
            print("Imagen recibida")
            open("recv.jpg", "wb").write(message["VALUE"])
        else:
            print("Mensaje desconocido")
            print(message)



    def send(self, tipe, data):
        data = dumps({"TIPE": tipe, "VALUE": data})
        self.socket.send(data)