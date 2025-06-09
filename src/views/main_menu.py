from src.generated.main_menu_ui import Ui_MainWindow
#import src.utils
from PyQt5.QtWidgets import QMainWindow, QApplication
import re

class MainMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
  
        self.ui.searchButton.clicked.connect(self.testButton)

    def testButton(self):
        search_key = re.split(r",\s*", self.ui.keywordSearch.toPlainText())
        print(search_key)

