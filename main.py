from PyQt5.QtGui import QPixmap,  QIcon
from PyQt5.QtWidgets import \
    QPushButton, QWidget, QDesktopWidget, QApplication, \
    QMainWindow, QLineEdit, QLabel, QScrollArea, QFrame, QGridLayout, QVBoxLayout, \
    QListWidget, QListWidgetItem
from PyQt5.QtCore import QSize
import User
from DB import UserDB


class Massenger(QMainWindow):
    def __init__(self, User):
        super().__init__()
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
        send_button.clicked.connect(self.get_message)

        search_icon_size = QSize(65,65)
        search_icon = QIcon('./pic/search.png')
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

    def get_message(self):
        message = self.write_box.text()
        if message == '':
            return
        else:
            item = QListWidgetItem()
            icon = QIcon(self.db.get_pic(self.User.get_name()))
            item.setIcon(icon)
            item.setText(message)
            self.message_box.setIconSize(QSize(50,50))
            self.message_box.addItem(item)
            self.write_box.clear()

    def render_image(self):
        pass

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

            visibale_image = QLabel()
            visibale_image.resize(65, 65)
            pixmap = QPixmap(users[i][3])
            visibale_image.setPixmap(pixmap)

            grid = QGridLayout()
            grid.addWidget(visibale_name, 0, 10)
            grid.addWidget(visible_last_messagge, 1, 10)
            grid.addWidget(visibale_image, 0,0, 0, 4)

            label.addLayout(grid)
        w = QWidget()
        w.setLayout(label)
        self.people_box.setWidget(w)

    def search_contacts(self):
        key = self.search_box.text()
        if key == '':
            key = 'all'
        print(key)
        self.render_contact(key)




    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     ex = Massenger()
#     sys.exit(app.exec_())