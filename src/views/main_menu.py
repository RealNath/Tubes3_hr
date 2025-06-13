from src.generated.main_menu_ui import Ui_MainWindow
from src.utils.loader import load_pdf
from PyQt5.QtWidgets import QMainWindow, QApplication
import re
from src.utils.kmp_search import kmp_search
from src.utils.bm_search import bm_search
from src.utils.ac_search import ac_search

class MainMenu(QMainWindow):
    def __init__(self, conn):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.conn = conn
        self.pdf_data = load_pdf(self.conn)
        
        self.ui.searchButton.clicked.connect(self.get_search_result)

    def get_search_result(self):
        keywords = re.split(r",\s*", self.ui.keywordSearch.toPlainText())
        if self.ui.radioKMP.isChecked():
            mode = "KMP"
        elif self.ui.radioBM.isChecked():
            mode = "BM"
        elif self.ui.radioAC.isChecked():
            mode = "AC"
        else:
            mode = "KMP"
        result_amount = self.ui.topMatchesNumber.value()
        self.search(keywords, mode, result_amount)

    def search(self, keywords, mode, result_amount):
        """
        Searches for keywords in the loaded PDF data using the specified algorithm.

        Args:
            keywords (list of str): List of keywords to search for.
            mode (str): Search algorithm ("KMP", "BM", or "AC").
            result_amount (int): Number of top results to return.

        Returns:
            list: [
                {
                    'detail_id': int,
                    'keywords': {keyword: occurrence, ...},
                    'total': int
                },
                ...
            ]
            Sorted by 'total' in descending order, limited to result_amount entries.
        """
        keywords = [kw.lower() for kw in keywords if kw]
        results = []
        if mode == "AC":
            for detail_id, data in self.pdf_data.items():
                text = data['pattern_match']
                ac_result = ac_search(text, keywords)
                kw_counts = {kw: len(ac_result.get(kw, [])) for kw in keywords}
                total = sum(kw_counts.values())
                results.append({
                    'detail_id': detail_id,
                    'keywords': kw_counts,
                    'total': total
                })
        else:
            for detail_id, data in self.pdf_data.items():
                text = data['pattern_match']
                kw_counts = {}
                for kw in keywords:
                    if mode == "KMP":
                        count = kmp_search(text, kw)
                    elif mode == "BM":
                        count = bm_search(text, kw)
                    else:
                        count = 0
                    kw_counts[kw] = count
                total = sum(kw_counts.values())
                results.append({
                    'detail_id': detail_id,
                    'keywords': kw_counts,
                    'total': total
                })
        # Sort by total matches, descending, and take top N
        results.sort(key=lambda x: x['total'], reverse=True)
        top_results = results[:result_amount]
        return top_results