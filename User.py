from PyQt5.QtWidgets import QMessageBox, QProgressBar, QFrame, QFileDialog, \
    QInputDialog, QPushButton, QWidget, \
    QDesktopWidget, QApplication, QMainWindow, \
    QLineEdit, QLabel, QGridLayout

from PyQt5.QtGui import QPixmap, QRegion


class User():

    def __init__(self, name, IP, to_send_IP):
        self.to_send_IP = to_send_IP
        self.IP = IP
        self.name = name

    def get_name(self):
        return self.name

    def get_send_IP(self):
        return self.to_send_IP

    def set_send_ip(self, new_send_ip):
        self.to_send_IP = new_send_ip
