from PyQt5 import Qt, QtCore, QtWidgets
from PyQt5.QtWidgets import *
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtGui import QDrag
from PyQt5.QtCore import QMimeData, pyqtSignal


class Button(Qt.QPushButton):
    left_click = pyqtSignal()
    right_click = pyqtSignal()

    def __init__(self, title, parent):
        super().__init__(title, parent)

    def mouseMoveEvent(self, e):
        if e.buttons() != Qt.Qt.RightButton:
            return
        mimeData = QMimeData()
        drag = QDrag(self)
        drag.setMimeData(mimeData)
        drag.setHotSpot(e.pos() - self.rect().topLeft())
        dropAction = drag.exec_(Qt.Qt.MoveAction)

    def mousePressEvent(self, event):
        buttom = event.button()
        if buttom == Qt.Qt.LeftButton:
            self.left_click.emit()
            print('шмяк по левой')
        if buttom == Qt.Qt.RightButton:
            self.right_click.emit()
            print('шмяк по правой')


class prog(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setAcceptDrops(True)
        self.button = QPushButton('Создать объект "Кнопка"', self)
        self.button.move(100, 65)
        self.button.clicked.connect(self.generate)
        self.spin = []

    def generate(self):
        button_d = Button('Button', self)
        button_d.move(150, 65)
        button_d.show()
        # button_d.left_click.connect(self.generate)
        button_d.right_click.connect(self.ident_but)
        self.spin.append(button_d)

    def ident_but(self):
        self.mov_but = self.sender()

    def dragEnterEvent(self, e):
        e.accept()

    def dropEvent(self, e):
        position = e.pos()
        self.mov_but.move(position)
        e.setDropAction(Qt.Qt.MoveAction)
        e.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = prog()
    ex.show()
    app.exec_()