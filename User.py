from PyQt5.QtWidgets import QMessageBox, QProgressBar, QFrame, QFileDialog, \
    QInputDialog, QPushButton, QWidget, \
    QDesktopWidget, QApplication, QMainWindow, \
    QLineEdit, QLabel, QGridLayout

from PyQt5.QtGui import QPixmap, QRegion


class User(QGridLayout):
    def __init__(self, name, profile_image, last_message):
        self.name = name
        self.profile_image = profile_image
        self.last_message = last_message
        self.render_user()

    def render_user(self):
        visibale_name = QLabel(self.name)
        visible_last_messagge = QLabel(self.last_message)

        visibale_image = QLabel(self)
        visibale_image.resize(65, 65)
        visibale_image.setFrameStyle(QFrame.Panel | QFrame.Plain)
        visibale_image.setLineWidth(2)
        visibale_image.setStyleSheet("border: 3px solid black; border-radius: 32px;")

        pixmap = QPixmap(self.profile_image)
        visibale_image.setPixmap(pixmap)

        grid = QGridLayout()
        grid.addWidget(visibale_name, 0, 1)
        grid.addWidget(visible_last_messagge, 2, 1)
        grid.addWidget(visibale_image, 0, 4, 0, 0)

        grid.show()
