import socket
from _thread import *
import json
import CONST
from subscriber import *
from client import CLient_socket
from DB import UserDB, MesagesDB

class Server(Subject):
    def __init__(self):
        self._state = None
        self._observers = []
        self.users_ip = []
        self.users_port = []
        self.Users = UserDB()
        self.attach(CLient_socket)
        self.start_server()

    def start_server(self):
        self.ServerSocket = socket.socket()
        self.ServerSocket.bind((CONST.HOST, CONST.PORT))
        self.ServerSocket.listen(7)
        while True:
            Client, address = self.ServerSocket.accept()
            self.users_ip.append(address[0])
            self.users_port.append(address[1])
            print('Connected to: ' + address[0] + ':' + str(address[1]))
            start_new_thread(self.threaded_client, (Client,))

    def close_server(self):
        self.ServerSocket.close()

    def threaded_client(self ,connection):
        while True:
            raw_data = connection.recv(2048)
            if not raw_data:
                continue
            data = json.loads(raw_data.decode("utf-8"))
            self.add_data_to_db(data)
            self.send_data(data, connection)
        connection.close()

    def add_data_to_db(self, data):
        print(data['from'], data['to'])
        if data['from'] > data['to']:
            self.Messanges = MesagesDB(data['from'], data['to'])
        else:
            self.Messanges = MesagesDB(data['to'], data['from'])

        self.Messanges.insetr_message(data['message'], data['from'])

    def attach(self, observer) -> None:
        print("Subject: Attached an observer.")
        self._observers.append(observer)

    def detach(self, observer) -> None:
        self._observers.remove(observer)

    def send_data(self, data, connection):
        send_ip = (self.Users.get_ip_by_id(data['to']))
        Json_str = json.dumps(data, ensure_ascii=False).encode("utf-8")
        i = self.users_ip.index(send_ip)
        connection.sendto(Json_str, (self.users_ip[i], self.users_port[i]))
        self._observers[0].get_data(self)


server = Server()
