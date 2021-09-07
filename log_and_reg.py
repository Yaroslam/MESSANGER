from PyQt5.QtWidgets import  QFrame, QFileDialog, QPushButton, \
    QDesktopWidget, QApplication, QMainWindow, \
    QLineEdit, QLabel
from PyQt5.QtGui import QPixmap
from style import Style
from CustomMessageWindow import MessageWindow
from main import Massenger
from client import CLient_socket
import sys
from CONST import get_image, compare_str, get_diveded_str
import DB
import User



class Login_or_Register(QMainWindow):
    def __init__(self):
        super().__init__()
        self.Socket = CLient_socket() #TODO add connection
        self.initUI()

    def initUI(self):
        self.setStyleSheet(Style.Window.window)
        self.reg_btn = QPushButton('register', self)
        self.reg_btn.resize(390, 70)
        self.reg_btn.move(15, 98)
        self.reg_btn.clicked.connect(self.click_reg)
        self.reg_btn.setStyleSheet(Style.button.log_reg)

        log_btn = QPushButton('login', self)
        log_btn.resize(390, 70)
        log_btn.move(15, 192)
        log_btn.clicked.connect(self.click_log)
        log_btn.setStyleSheet(Style.button.log_reg)

        self.setFixedSize(420, 420)
        self.center()
        self.setWindowTitle('Login')
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def click_reg(self):
        self.reg_btn.setStyleSheet(Style.button.log_reg)
        self.close()
        self.next = Get_data(True, self.Socket)

    def click_log(self):
        self.close()
        self.next = Get_data(False, self.Socket)


class Get_data(QMainWindow):
    def __init__(self, isReg, socket):
        super().__init__()
        self.Socket = socket
        self.isREG = isReg
        self.db = DB.UserDB()
        self.initUI()

    def initUI(self):
        self.setStyleSheet(Style.Window.window)
        self.login_label = QLineEdit(self)
        self.login_label.move(15, 98)
        self.login_label.resize(390, 70)
        self.login_label.setStyleSheet(Style.Label.label)

        self.password_label = QLineEdit(self)
        self.password_label.move(15, 254)
        self.password_label.resize(390, 70)
        self.password_label.setStyleSheet(Style.Label.label)

        title_log = QLabel("LOGIN", self)
        title_log.move(158, 44)
        title_log.resize(105, 44)
        title_log.setStyleSheet(Style.Text.text)

        title_pass = QLabel("PASSWORD", self)
        title_pass.resize(195, 52)
        title_pass.move(113, 185)
        title_pass.setStyleSheet(Style.Text.text)

        self.ok_btn = QPushButton('ok', self)
        self.ok_btn.move(147, 354)
        self.ok_btn.resize(125, 40)
        self.ok_btn.clicked.connect(self.next_window)
        self.ok_btn.setStyleSheet(Style.button.ok)

        self.setFixedSize(420, 420)
        self.center()
        self.setWindowTitle('Login')
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def next_window(self):
        if self.login_label.text() == '' or self.password_label.text() == '':
            msg = MessageWindow('empty log')
            msg.exec()
            return
        name = self.login_label.text()
        if self.isREG:
            self.Socket.send_request("ADD_NEW_USER", [self.login_label.text(), self.password_label.text()])
            self.User = User.User(name, self.db.get_id(name), None) #TODO rewrite, crete user on server
            self.close()
            self.next = Get_image(self.User, self.Socket)
        else:
            self.Socket.send_request("GET_USER_PASS", [self.login_label.text()])
            user_pass = self.Socket.get_response()
            if user_pass == self.password_label.text():
                self.User = User.User(name, self.db.get_id(name), None) #TODO rewrite, crete user on server
                self.close()
                self.next = Massenger(self.User, self.Socket)


class Get_image(QMainWindow):
    def __init__(self, User, socket):
        super().__init__()
        self.Socket = socket
        self.User = User
        self.db = DB.UserDB()
        self.initUI()

    def get_path(self):
        i = 1
        wb_patch = QFileDialog.getOpenFileName()[0]
        while (compare_str(get_diveded_str(wb_patch, '.')) != True) and (i < 2):
            i += 1
            wb_patch = QFileDialog.getOpenFileName()[0]
            if i == 2:
                return 'PASS'

        new_image_path = get_image(self.User.get_name(), wb_patch)
        self.Socket.send_request("SET_IMAGE", [new_image_path])

        pixmap = QPixmap(new_image_path)
        self.label.setPixmap(pixmap)
        return new_image_path

    def initUI(self):
        self.setStyleSheet(Style.Window.window)
        get_path_btn = QPushButton('выберите изображение', self)
        get_path_btn.clicked.connect(self.get_path)
        get_path_btn.resize(150,30)
        get_path_btn.move(135, 260)

        ok_btn = QPushButton('ok', self)
        ok_btn.move(160, 310)
        ok_btn.clicked.connect(self.next_window)

        self.label = QLabel(self)
        self.label.resize(156, 156)
        self.label.setFrameStyle(QFrame.Panel | QFrame.Plain)
        self.label.setLineWidth(2)
        self.label.setStyleSheet("border: 3px solid black; border-radius: 75px;")
        self.label.move(135,50)

        self.setFixedSize(420, 350)
        self.center()
        self.setWindowTitle('Login')
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def next_window(self):
        self.close()
        self.next = Massenger(self.User, self.Socket)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Login_or_Register()
    sys.exit(app.exec_())
