from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QInputDialog,\
    QPushButton, QWidget, QDesktopWidget, QApplication, \
    QMainWindow, QLineEdit, QLabel
import sys
from CONST import *

class Massenger(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        label = QLabel(self)
        pixmap = QPixmap('maxresdefault.jpg')
        label.setPixmap(pixmap)
        label.setFixedSize(420, 420)

        self.setFixedSize(1440, 1024)
        self.setWindowTitle('Login')
        self.show()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Massenger()
    sys.exit(app.exec_())