import socket
from _thread import *
import json
import CONST
from DB import UserDB, MesagesDB

#TODO:
#   4)load users pics
#       4.1)check is client has all users pics


class Server():
    def __init__(self):
        self._state = None
        self.users_ip = []
        self.users_port = []
        self.Users = UserDB()
        self.start_server()

    def start_server(self):
        self.ServerSocket = socket.socket()
        self.ServerSocket.bind((CONST.HOST, CONST.PORT))
        self.ServerSocket.listen(7)
        while True:
            Client, address = self.ServerSocket.accept()
            self.users_ip.append(address[0])
            self.users_port.append(address[1])
            print(self.users_ip, self.users_port)
            print('Connected to: ' + address[0] + ':' + str(address[1]))
            start_new_thread(self.threaded_client, (Client,address,))

    def close_server(self):
        self.ServerSocket.close()

    def threaded_client(self ,connection, address):
        while True:
            raw_data = connection.recv(10000)
            if not raw_data:
                continue
            print('get data from user')
            request = json.loads(raw_data.decode("utf-8"))
            self.request_handler(request, connection, address)
        connection.close()

    def add_data_to_db(self, data):
        if data['from'] > data['to']:
            Messanges = MesagesDB(data['from'], data['to'])
        else:
            Messanges = MesagesDB(data['to'], data['from'])

        Messanges.insetr_message(data['message'], data['from'])

    def send_data(self, data, connection):
        send_ip = (self.Users.get_ip_by_id(data['to']))
        Json_str = json.dumps(data, ensure_ascii=False).encode("utf-8")
        i = self.users_ip.index(send_ip)
        connection.sendto(Json_str, (self.users_ip[i], self.users_port[i]))

    def compare_last_messages(self, request):
        messages_info = {'messages': [], 'pic': []}
        if request['exstra_param'][0] > request['exstra_param'][1]:
            Messanges = MesagesDB(str(request['exstra_param'][0]), str(request['exstra_param'][1]))
        else:
            Messanges = MesagesDB(str(request['exstra_param'][1]), str(request['exstra_param'][0]))
        for i in Messanges.select_100_masseges(1, 0):
            pic = self.Users.get_pic_by_id(i[1])
            message = i[2]
            messages_info['messages'].append(message)
            messages_info['pic'].append(pic)
            messages_info['to'] = request['exstra_param'][1]
        return messages_info

    def register_new_user(self, login, password):
        self.Users.insert_user_info(login, password)

    def get_user_password(self, name):
        return self.Users.get_password(name)

    def compare_reaponse(self):
        pass

    def send_response(self, response, response_param, connection):
        send_ip = response_param['send_ip']
        send_port = response_param['port']
        if "PASSWORD" in response_param.keys(): #TODO вынести в отдельную функцию
            response["PASSWORD"] = response_param["PASSWORD"]
        if "USERS" in response_param.keys():
            response["USERS"] = response_param["USERS"]
        response = json.dumps(response, ensure_ascii=False).encode("utf-8")
        connection.sendto(response, (send_ip, send_port))

    def load_users(self, key):
        if key == 'all':
            return self.Users.select_all_data()
        else:
            return self.Users.get_users_by_key(key)


    def request_handler(self, request, connection, address):
        if request['request'] == 'LOAD100':
            print(request)
            messages_info = self.compare_last_messages(request)
            self.send_data(messages_info, connection)
        elif request['request'] == 'NEW_MESSAGE':
            raw_data = connection.recv(2048)
            data = json.loads(raw_data.decode("utf-8"))
            self.add_data_to_db(data)
            self.send_data(data, connection)
        elif request['request'] == 'LOAD_IMAGES':
            pass
        elif request['request'] == "ADD_NEW_USER":
            self.register_new_user(request["exstra_param"][0], request["exstra_param"][1])
        elif request['request'] == "SET_IMAGE":
            self.Users.insert_user_pic(request["exstra_param"][0])
        elif request['request'] == "LOAD_USERS":
            users = self.load_users(request["exstra_param"][0])
            self.send_response({"response": "OK"},
                               {'send_ip': address[0], 'send_port': address[1], "USERS": users}, connection)
        elif request['request'] == "GET_USER_PASS":
            password = self.get_user_password(request["exstra_param"][0])
            self.send_response({"response": "OK"},
                               {'send_ip': address[0], 'send_port': address[1], 'PASSWORD': password}, connection)


server = Server()
