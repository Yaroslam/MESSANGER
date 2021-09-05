from PyQt5.QtGui import QPixmap,  QIcon
from PyQt5.QtWidgets import \
    QPushButton, QWidget, QDesktopWidget, QApplication, \
    QMainWindow, QLineEdit, QLabel, QScrollArea, QFrame, QGridLayout, QVBoxLayout, \
    QListWidget, QListWidgetItem, QButtonGroup
from PyQt5.QtCore import QSize
from subscriber import Observer
from client import CLient_socket
import os
import CONST
from DB import UserDB, MesagesDB
from MyQButton import  MyQButton
from style import Style
import threading


class Massenger(QMainWindow):
    def __init__(self, User):
        super().__init__()
        print('OK1')
        self.client_sock = CLient_socket()
        print('OK2')
        self.User = User
        print('OK3')
        self.db = UserDB()
        print('OK4')
        self.initUI()
        print('OK5')
        self.render_contact('all')
        print('OK6')
        self.db.insert_user_IP(self.client_sock.connection())
        print('OK7')
        self.start_thread_send()
        print('OK8')
        self.start_thread_get()
        print('OK9')


    def initUI(self):
        self.setStyleSheet(Style.Window.window)
        self.write_box = QLineEdit(self)
        self.write_box.move(470, 924)
        self.write_box.resize(843, 75)
        self.write_box.setStyleSheet(Style.Label.send)

        self.message_box = QListWidget(self)
        self.message_box.move(470, 10)
        self.message_box.resize(951, 904)
        self.message_box.setStyleSheet(Style.Window.dilog)

        self.search_box = QLineEdit(self)
        self.search_box.move(85, 10)
        self.search_box.resize(365, 65)
        self.search_box.setStyleSheet(Style.Label.search_label)

        self.people_box = QScrollArea(self)
        self.people_box.move(0, 100)
        self.people_box.resize(460, 924)
        self.people_box.setStyleSheet(Style.Window.contacts)

        send_button = QPushButton('send', self)
        send_button.resize(65, 65)
        send_button.move(868+460+10, 926)
        send_button.clicked.connect(self.send_message)
        send_button.setStyleSheet(Style.button.send)

        search_icon_size = QSize(65,65)
        search_icon = QIcon('./work_pic/lupa.jpg')
        search_button = QPushButton(self)
        search_button.setIcon(search_icon)
        search_button.setStyleSheet('border:none')
        search_button.setIconSize(search_icon_size)
        search_button.move(10,10)
        search_button.resize(65,65)
        search_button.clicked.connect(self.search_contacts)

        self.setFixedSize(1440, 1024)
        self.center()
        self.setWindowTitle('Login')
        self.show()

    def send_message(self):
        message = self.write_box.text()
        print(self.User.get_send_id())
        print(self.start_diolog())
        if message == '':
            self.message_box.scrollToBottom()
        elif self.start_diolog() == None:
            message = "Подключитесь к диалогу"
            item = QListWidgetItem()
            icon = QIcon(self.db.get_pic(self.User.get_name()))
            item.setIcon(icon)
            item.setText(message)
            self.message_box.setIconSize(QSize(50,50))
            self.message_box.addItem(item)
            self.write_box.clear()
            self.message_box.scrollToBottom()
        elif self.start_diolog() == "OK":
            item = QListWidgetItem()
            icon = QIcon(self.db.get_pic(self.User.get_name()))
            data = self.client_sock.compare_data(self.User.get_own_id(),self.User.get_send_id(), message)
            self.client_sock.send_data(data)
            item.setIcon(icon)
            item.setText(message)
            self.message_box.setIconSize(QSize(50, 50))
            self.message_box.addItem(item)
            self.message_box.scrollToBottom()
            self.write_box.clear()

    def render_messages(self):
        while True:
            data = self.client_sock.get_data()
            print(data)
            message_info = data['message']
            item = QListWidgetItem()
            icon = QIcon(self.db.get_pic_by_id(data['from']))
            item.setIcon(icon)
            item.setText(message_info)
            self.message_box.setIconSize(QSize(50, 50))
            self.message_box.addItem(item)

    def render_contact(self, key_word):
        label = QVBoxLayout()

        if key_word == 'all':
            users = self.db.select_all_data()
            count_of_users = len(users)
        else:
            users = self.db.get_users_by_key(key_word)
            count_of_users = len(users)

        for i in range(count_of_users):
            if users[i][1] == self.User.get_name():
                continue
            visibale_name = QLabel(users[i][1])
            visibale_image = QIcon(users[i][3])
            contact_button = MyQButton(users[i][0])
            contact_button.clicked.connect(self.go_to_dilog)
            contact_button.setCheckable(True)
            contact_button.setIcon(visibale_image)
            contact_button.setStyleSheet('border:none')
            contact_button.setIconSize(QSize(65,65))
            contact_button.resize(65, 65)

            grid = QGridLayout()
            grid.addWidget(visibale_name, 0, 10)
            grid.addWidget(contact_button, 0,0, 0, 4)
            label.addLayout(grid)

        w = QWidget()
        w.setLayout(label)
        w.setStyleSheet('border:none')
        self.people_box.setWidget(w)

    def go_to_dilog(self):
        self.message_box.clear()
        sndr = self.sender()
        to_id = sndr.get_id()
        from_id = self.db.get_id(self.User.get_name())
        print(f"./{CONST.DB_PATH}/{from_id}to{to_id}")
        if from_id > to_id:
            if os.path.exists(f"./{CONST.DB_PATH}/{from_id}to{to_id}"):
                pass
            else:
                self.message_db = MesagesDB(from_id, to_id)
        else:
            if os.path.exists(f"./{CONST.DB_PATH}/{to_id}to{from_id}"):
                pass
            else:
                self.message_db = MesagesDB(to_id, from_id)
        self.User.set_send_id(to_id)
        self.render_previous_messages()
        self.message_box.scrollToBottom()
        return to_id

    def render_previous_messages(self):
        previous = self.message_db.select_all_masseges()
        print(previous)
        for i in previous:
            item = QListWidgetItem()
            icon = QIcon(self.db.get_pic_by_id(i[1]))
            item.setIcon(icon)
            item.setText(i[2])
            self.message_box.setIconSize(QSize(50, 50))
            self.message_box.addItem(item)


    def search_contacts(self):
        key = self.search_box.text()
        if key == '':
            key = 'all'
        print(key)
        self.render_contact(key)

    def start_diolog(self):
        if self.User.get_send_id() == None:
            return None
        else:
            return "OK"


    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def start_thread_send(self):
        background_thread = threading.Thread(target=self.send_message)
        background_thread.daemon = True
        background_thread.start()

    def start_thread_get(self):
        background_thread = threading.Thread(target=self.render_messages)
        background_thread.daemon = True
        background_thread.start()


# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     ex = Massenger()
#     sys.exit(app.exec_())