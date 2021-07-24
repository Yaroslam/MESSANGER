from PyQt5.QtWidgets import  QFrame, QFileDialog, QPushButton, \
    QDesktopWidget, QApplication, QMainWindow, \
    QLineEdit, QLabel
from PyQt5.QtGui import QPixmap
from main import Massenger
import sys
from CONST import get_image, compare_str, get_diveded_str
import DB
import User



class Login_or_Register(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        reg_btn = QPushButton('register', self)
        reg_btn.resize(390, 70)
        reg_btn.move(15, 98)
        reg_btn.clicked.connect(self.click_reg)

        log_btn = QPushButton('login', self)
        log_btn.resize(390, 70)
        log_btn.move(15, 192)
        log_btn.clicked.connect(self.click_log)

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
        self.close()
        self.next = Get_data(True)

    def click_log(self):
        self.close()
        self.next = Get_data(False)


class Get_data(QMainWindow):
    def __init__(self, isReg):
        super().__init__()
        self.isREG = isReg
        self.db = DB.UserDB()
        self.initUI()

    def initUI(self):
        self.login_label = QLineEdit(self)
        self.login_label.move(15, 65)
        self.login_label.resize(390, 30)

        self.password_label = QLineEdit(self)
        self.password_label.move(15, 135)
        self.password_label.resize(390, 30)

        title_log = QLabel("Enter login", self)
        title_log.move(15, 40)

        title_pass = QLabel("Enter password", self)
        title_pass.move(15, 110)

        self.ok_btn = QPushButton('ok', self)
        self.ok_btn.move(160, 310)
        self.ok_btn.clicked.connect(self.next_window)

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
        if self.login_label.text() == '' or self.password_label.text() == '':
            return
        self.User = User.User(self.login_label.text())
        if self.isREG:
            self.db.insert_user_info(self.login_label.text(), self.password_label.text())
            self.close()
            self.next = Get_image(self.User)
        else:
            if self.db.get_password(self.login_label.text()) == self.password_label.text():
                self.close()
                self.next = Massenger(self.User)


class Get_image(QMainWindow):
    def __init__(self, User):
        super().__init__()
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
        self.db.insert_user_pic(new_image_path)

        pixmap = QPixmap(new_image_path)
        self.label.setPixmap(pixmap)
        return new_image_path

    def initUI(self):
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
        self.next = Massenger(self.User)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Login_or_Register()
    sys.exit(app.exec_())
