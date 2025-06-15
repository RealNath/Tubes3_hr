from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget
from PyQt5.QtCore import Qt
from src.generated.summary_menu import Ui_SummaryWindow

class SummaryPage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_SummaryWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Summary")

