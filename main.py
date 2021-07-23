from PyQt5.QtGui import QPixmap, QStandardItemModel, QIcon, QStandardItem
from PyQt5.QtWidgets import QInputDialog,\
    QPushButton, QWidget, QDesktopWidget, QApplication, \
    QMainWindow, QLineEdit, QLabel, QScrollArea, QFrame, QGridLayout, QVBoxLayout, \
    QListView, QListWidget, QListWidgetItem
from PyQt5.QtCore import QSize
import sys
import User
from DB import UserDB


class Massenger(QMainWindow):
    def __init__(self, User):
        super().__init__()
        self.User = User
        self.db = UserDB()
        self.initUI()
        self.render_contact()

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

        search_image = QPixmap(self.db.get_pic(self.User.get_name()))
        search_image_label = QLabel(self)
        search_image_label.move(10,10)
        search_image_label.resize(65,65)
        search_image_label.setPixmap(search_image)

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

    def render_contact(self):
        label = QVBoxLayout()
        for i in range(10):
            visibale_name = QLabel('boris')
            visible_last_messagge = QLabel('soxi')

            visibale_image = QLabel()
            visibale_image.resize(65, 65)
            visibale_image.setFrameStyle(QFrame.Panel | QFrame.Plain)
            visibale_image.setLineWidth(2)
            visibale_image.setStyleSheet("border: 3px solid black; border-radius: 32px;")

            pixmap = QPixmap('resize-output.png')
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
        pass




    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     ex = Massenger()
#     sys.exit(app.exec_())