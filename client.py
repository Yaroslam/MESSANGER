import socket
import json
import CONST
from subscriber import *
import threading

#TODO:
#   2)get_response
#       2.1)what_would_client_do
#   3)cover comments


class CLient_socket():
    def __init__(self):
        self.Client_socket = socket.socket()
        print(1)

    def connection(self):
        try:
            self.Client_socket.connect((CONST.HOST, CONST.PORT))
        except socket.error as e:
            print(str(e))
        new_ip =  self.Client_socket.getsockname()[0]
        return new_ip

    def compare_data(self, from_id, to_id, message):
        data = {}
        data["from"] = from_id
        data["to"] = to_id
        data["message"] = message
        return data

    def send_data(self, data):
        Json_str = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.Client_socket.send(Json_str)

    def close_connection(self):
        drop_ip = self.Client_socket.getsockname()[0]
        self.Client_socket.close()
        return drop_ip

    def get_data(self):
            data = self.Client_socket.recv(10000)
            data = json.loads(data.decode("utf-8"))
            print('get data from server')
            return data

    def send_request(self, request, exstra_param):
        data = {}
        data['request'] = request
        if exstra_param != None:
            data['exstra_param'] = exstra_param
        self.send_data(data)
