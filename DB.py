from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QRegion


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(500, 500)
        self.mainFrame = QtWidgets.QFrame(Form)
        self.mainFrame.setGeometry(QtCore.QRect(10, 10, 481, 481))
        self.mainFrame.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.mainFrame.setObjectName("mainFrame")
        QtCore.QMetaObject.connectSlotsByName(Form)

        Form.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        Form.setStyleSheet("QFrame#mainFrame {\n"
                           "    border: 5px solid grey;\n"
                           "    border-radius: 240px;\n"
                           "    background-color: rgba(255, 0, 0, 50);\n"
                           "}\n"
                           "QWidget#Form {\n"
                           "    background-color: rgba(255, 255, 255, 0);\n"
                           "    border: 5px solid grey;\n"
                           "    border-radius: 250px;\n"
                           "}")
        self.mainFrame.mouseDoubleClickEvent = lambda event: QtWidgets.qApp.quit()
        Form.setWindowOpacity(0.4)
        self.mainFrame.setWindowOpacity(1)


class MainWindow(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super().__init__()

        self.setupUi(self)

        self.region_and_mask()

    def region_and_mask(self):
        my_region = QRegion(self.rect(), QRegion.Ellipse)
        self.setMask(my_region)


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())