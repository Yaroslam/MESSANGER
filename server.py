import socket
from _thread import *
import json
import CONST
from DB import UserDB, MesagesDB

class Server():
    def __init__(self):
        self.users_ip = []
        self.Users = UserDB()
        self.start_server()

    def start_server(self):
        self.ServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.ServerSocket.bind((CONST.HOST, CONST.PORT))
        except socket.error as e:
            print(str(e))
        self.ServerSocket.listen(5)
        while True:
            Client, address = self.ServerSocket.accept()
            self.users_ip.append(address[0])
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
        connection.close()

    def add_data_to_db(self, data):
        print(data['from'], data['to'])
        if data['from'] > data['to']:
            self.Messanges = MesagesDB(data['from'], data['to'])
        else:
            self.Messanges = MesagesDB(data['to'], data['from'])

        self.Messanges.insetr_message(data['message'], data['from'])
        send_ip = self.Users.get_ip_by_id(data['to'])

server = Server()
