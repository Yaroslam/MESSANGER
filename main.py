from PyQt5.QtGui import QPixmap,  QIcon
from PyQt5.QtWidgets import \
    QPushButton, QWidget, QDesktopWidget, QApplication, \
    QMainWindow, QLineEdit, QLabel, QScrollArea, QFrame, QGridLayout, QVBoxLayout, \
    QListWidget, QListWidgetItem, QButtonGroup
from PyQt5.QtCore import QSize
import User
import os
import CONST
from DB import UserDB, MesagesDB
from MyQButton import  MyQButton

#TODO
# написать сервер
    #TODO
    # иформация приходит в виде JSON
    # постоянно следит за поступлением новых сигналов
    # отпраляет пользователю, которому пришло сообщение уведомление, и выводит сообщение через гет_мессаге
    # подгрузка предыдущих сообщений
#TODO
# написать гет_мессаге

#TODO
# разобраться с классом USER




class Massenger(QMainWindow):
    def __init__(self, User):
        super().__init__()
        self.contacts_butn_group = QButtonGroup()
        self.User = User
        self.db = UserDB()
        self.initUI()
        self.render_contact('all')

    def initUI(self):
        self.write_box = QLineEdit(self)
        self.write_box.move(470, 924)
        self.write_box.resize(843, 75)

        self.message_box = QListWidget(self)
        self.message_box.move(470, 10)
        self.message_box.resize(951, 904)

        self.search_box = QLineEdit(self)
        self.search_box.move(85, 10)
        self.search_box.resize(365, 65)
        self.search_box.setStyleSheet("QLineEdit { background: rgb(0, 255, 255); border: 3px solid black; border-radius: 20px; }")

        self.people_box = QScrollArea(self)
        self.people_box.move(0, 100)
        self.people_box.resize(460, 924)

        send_button = QPushButton('send', self)
        send_button.resize(65, 65)
        send_button.move(868+460+10, 924)
        send_button.clicked.connect(self.send_message)

        search_icon_size = QSize(65,65)
        search_icon = QIcon('./pic/as.png')
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
        print(self.User.get_send_IP())
        print(self.start_diolog())
        if message == '':
            return
        elif self.start_diolog() == None:
            message = "Подключитесь к диалогу"
            item = QListWidgetItem()
            icon = QIcon(self.db.get_pic(self.User.get_name()))
            item.setIcon(icon)
            item.setText(message)
            self.message_box.setIconSize(QSize(50,50))
            self.message_box.addItem(item)
            self.write_box.clear()
            return
        elif self.start_diolog() == "OK":
            item = QListWidgetItem()
            icon = QIcon(self.db.get_pic(self.User.get_name()))
            item.setIcon(icon)
            item.setText(message)
            self.message_box.setIconSize(QSize(50, 50))
            self.message_box.addItem(item)
            self.message_db.insetr_message(message, 4)
            self.write_box.clear()


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
            visible_last_messagge = QLabel('soxi')
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
            grid.addWidget(visible_last_messagge, 1, 10)
            grid.addWidget(contact_button, 0,0, 0, 4)
            label.addLayout(grid)

        w = QWidget()
        w.setLayout(label)
        self.people_box.setWidget(w)

    def go_to_dilog(self):
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
        self.User.set_send_ip(to_id)


    def search_contacts(self):
        key = self.search_box.text()
        if key == '':
            key = 'all'
        print(key)
        self.render_contact(key)

    def start_diolog(self):
        if self.User.get_send_IP() == None:
            return None
        else:
            return "OK"


    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     ex = Massenger()
#     sys.exit(app.exec_())