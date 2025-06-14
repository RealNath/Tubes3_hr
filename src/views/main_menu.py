from src.generated.main_menu_ui import Ui_MainWindow
from src.utils.loader import load_pdf
from src.generated.result_card import Ui_resultCard 
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget
from PyQt5.QtCore import Qt
import re
from src.utils.kmp_search import kmp_search
from src.utils.bm_search import bm_search
from src.utils.ac_search import ac_search
import time

class ResultCard(QWidget):
    def __init__(self, name, matches_number, matched_keywords):
        #Summary & link later
        super().__init__()
        self.setFixedSize(900, 500)
        self.ui = Ui_resultCard()
        self.ui.setupUi(self)

        self.ui.name.setText(name)
        self.ui.matches_number.setText(f"{matches_number} {"matches" if matches_number > 1 else "match"}")
        self.ui.matched_keywords.setText(matched_keywords)
                                    
class MainMenu(QMainWindow):
    def __init__(self, conn):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.conn = conn

        print("Loading PDF data...")
        start_time = time.time()
        self.pdf_data = load_pdf(self.conn)
        print(f"PDF data loaded in {time.time() - start_time:.4f} seconds")
        
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

        print(f"Searching for keywords: {keywords} using {mode} algorithm, top {result_amount} results")
        start_time = time.time()
        results = self.search(keywords, mode, result_amount)
        search_time = time.time() - start_time
        print(f"Search completed in {search_time:.4f} seconds")

        self.display_result(results, search_time)

    def display_result(self, results, search_time):
        self.clear_grid_layout()
        self.ui.searchResultData.setText(f"Loading time : {search_time:.3f} s")
        for i, result in enumerate(results):
            name = result.get('applicant_name')
            matches_number = result.get('total')
            matched_keywords = ""
            keywords_dict = result.get('keywords')
            for j, (key, value) in enumerate(keywords_dict.items()):
                matched_keywords += f"{j+1}. {key} : {value} {"occurences" if value > 1 else "occurence"}"

            result_card = ResultCard(name, matches_number, matched_keywords)
            row = i//3
            col = i%3
            self.ui.searchResult.addWidget(result_card, row, col, Qt.AlignTop | Qt.AlignLeft)

    def clear_grid_layout(self):
        """
        Clears all widgets from a QGridLayout.
        Ensures proper deletion of widgets to prevent memory leaks.
        """
        if self.ui.searchResult is None:
            return

        # Iterate backwards to safely remove items.
        # Alternatively, you can always takeAt(0) repeatedly as shown in the previous answer.
        # Looping backward is generally more intuitive for lists where indices change.
        # For QLayouts, takeAt(0) is often used because it simplifies index management.

        # Method 1: Using takeAt(0) repeatedly (most common for QLayouts)
        while self.ui.searchResult.count() > 0:
            item = self.ui.searchResult.takeAt(0)
            if item.widget():
                widget = item.widget()
                widget.setParent(None) # Unparent the widget
                widget.deleteLater()   # Schedule for deletion
            del item # Delete the QLayoutItem itself


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
                    'applicant_name': str,
                    'keywords': {keyword: occurrence, ...},
                    'total': int
                },
                ...
            ]
            Sorted by 'total' in descending order, limited to result_amount entries.
        """
        results = []
        cursor = self.conn.cursor()

        if mode == "AC":
            for detail_id, data in self.pdf_data.items():
                text = data['pattern_match']

                try:
                    ac_result = ac_search(text, [kw.lower() for kw in keywords])
                except ValueError as e:
                    print(f"Error searching with Aho-Corasick for detail_id {detail_id}: {e}")
                    continue

                kw_counts = {kw: len(ac_result.get(kw.lower(), [])) for kw in keywords}
                total = sum(kw_counts.values())

                if total > 0:
                    cursor.execute(
                        "SELECT first_name, last_name FROM ApplicationDetail NATURAL JOIN ApplicantProfile WHERE detail_id = %s",
                        (detail_id,)
                    )
                    applicant = cursor.fetchone()
                    applicant_name = f"{applicant[0]} {applicant[1]}" if applicant else "Unknown"
                    results.append({
                        'detail_id': detail_id,
                        'applicant_name': applicant_name,
                        'keywords': kw_counts,
                        'total': total
                    })

        else:
            for detail_id, data in self.pdf_data.items():
                text = data['pattern_match']
                kw_counts = {}

                for kw in keywords:
                    try:
                        if mode == "KMP":
                            count = kmp_search(text, kw.lower())
                        else:
                            count = bm_search(text, kw.lower())
                    except ValueError as e:
                        print(f"Error searching for keyword '{kw}' in detail_id {detail_id}: {e}")
                        continue
                    kw_counts[kw] = count
                total = sum(kw_counts.values())

                if total > 0:
                    cursor.execute(
                        "SELECT first_name, last_name FROM ApplicationDetail NATURAL JOIN ApplicantProfile WHERE detail_id = %s",
                        (detail_id,)
                    )
                    applicant = cursor.fetchone()
                    applicant_name = f"{applicant[0]} {applicant[1]}" if applicant else "Unknown"
                    results.append({
                        'detail_id': detail_id,
                        'applicant_name': applicant_name,
                        'keywords': kw_counts,
                        'total': total
                    })

        cursor.close()

        # Sort by total matches, descending, and take top N
        results.sort(key=lambda x: x['total'], reverse=True)
        top_results = results[:result_amount]
        for result in top_results: print(result)
        return top_results
    

