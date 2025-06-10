from src.generated.main_menu_ui import Ui_MainWindow
from src.generated.result_card import Ui_resultCard 
#import src.utils
from src.controller.SearchController import *
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
        mode = "KMP" if self.ui.modeToggle.value() == 0 else "BM"
        result_amount = self.ui.topMatchesNumber.value()
        self.cv_search(keywords, mode, result_amount)

    def renderResult(results, keywords):
        pass
        #Results should be array of dictionary, 
        #Dictionary have : Name, total search, occurence for each keyowrd (summary, link) <- later
        #Put data in label below "Results"
        #Get top matches number
        #For each, make a result car, with the data from searches
        #Put it in grid, 3x3 

    

