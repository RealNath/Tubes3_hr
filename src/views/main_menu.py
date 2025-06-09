from src.generated.main_menu_ui import Ui_MainWindow
#import src.utils
from PyQt5.QtWidgets import QMainWindow, QApplication
import re

class MainMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
  
        self.ui.searchButton.clicked.connect(self.get_search_result)

    def get_search_result(self):
        keywords = re.split(r",\s*", self.ui.keywordSearch.toPlainText())
        mode = "KMP" if self.modeToggle.value() == 0 else "BP"
        result_amount = self.topMatchesNumber.value()
        self.search(keywords, mode, result_amount)


    def search(keywords, mode, result_amount):
        pass

