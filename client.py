import socket
import json
import CONST
from subscriber import *

class CLient_socket(Observer, Subject):
    def __init__(self):
        from main import Massenger
        self._observers = []
        self.attach(Massenger)
        self.Client_socket = socket.socket()

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
        data = self.Client_socket.recv(1024)
        if not data:
            return 0
        else:
            self._observers[0].render_messages(self, data)

    def attach(self, observer) -> None:
        print("Subject: Attached an observer.")
        self._observers.append(observer)

    def detach(self, observer) -> None:
        self._observers.remove(observer)

