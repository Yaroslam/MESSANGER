from PyQt5.QtWidgets import QPushButton

class MyQButton(QPushButton):

    def __init__(self, id):
        super().__init__()
        self.id = id

    def get_id(self):
        return self.id