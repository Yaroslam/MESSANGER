from PyQt5.QtWidgets import QMessageBox, QProgressBar, QFrame, QFileDialog, \
    QInputDialog, QPushButton, QWidget, \
    QDesktopWidget, QApplication, QMainWindow, \
    QLineEdit, QLabel, QGridLayout

from PyQt5.QtGui import QPixmap, QRegion


class User():

    def __init__(self, name, id, to_send_id):
        self.to_send_id = to_send_id
        self.id = id
        self.name = name

    def get_name(self):
        return self.name

    def get_send_id(self):
        return self.to_send_id

    def set_send_id(self, new_send_id):
        self.to_send_id = new_send_id

    def get_own_id(self):
        return self.id
