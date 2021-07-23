from PyQt5.QtWidgets import QMessageBox, QProgressBar, QFrame, QFileDialog, \
    QInputDialog, QPushButton, QWidget, \
    QDesktopWidget, QApplication, QMainWindow, \
    QLineEdit, QLabel, QGridLayout

from PyQt5.QtGui import QPixmap, QRegion


class User():
    def __init__(self, name):
        self.name = name

    def get_name(self):
        return self.name


