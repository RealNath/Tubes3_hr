from PyQt5.QtCore import (
    QObject, pyqtSignal, Qt
)

class ApplicationDetailModel(QObject):
    def __init__(self):
        super().__init__()