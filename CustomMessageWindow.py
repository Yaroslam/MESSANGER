from PyQt5.QtWidgets import QMessageBox, QPushButton
from style import Style
from CONST import MESSAGES_PIC, MESSAGES_TEXT

class MessageWindow(QMessageBox):
    def __init__(self, message_type):
        super().__init__()
        self.init_info(message_type)
        self.initUI()

    def initUI(self):
        self.setStyleSheet(Style.button.Qmessagebutton)
    def init_info(self, message_type):
        self.setText(MESSAGES_TEXT[message_type])

