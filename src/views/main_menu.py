from src.generated.main_menu import Ui_MainWindow
from src.views.summary_menu import SummaryPage
from src.utils.loader import load_pdf
from src.generated.result_card import Ui_resultCard 
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QMessageBox
from PyQt5.QtCore import Qt
import re
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import QUrl
from src.utils.kmp_search import kmp_search
from src.utils.bm_search import bm_search
from src.utils.ac_search import ac_search
from src.utils.fuzzy_search import fuzzy_search
import time
import os

class ResultCard(QWidget):
    def __init__(self, applicant_id, name, matches_number, matched_keywords):
        #Summary & link later
        super().__init__()
        self.id = applicant_id
        self.setMinimumSize(900, 500)
        self.ui = Ui_resultCard()
        self.ui.setupUi(self)

        self.ui.name.setText(name)
        self.ui.matches_number.setText(f"{matches_number} {"matches" if matches_number > 1 else "match"}")
        self.ui.matched_keywords.setText(matched_keywords)

        #!GMN CARANYA
        self.pdf_path = None
        #
        self.ui.viewPDF.clicked.connect(self.go_to_pdf)
        self.ui.viewSummary.clicked.connect(self.go_to_summary)

        self.summary_window = None

    def go_to_pdf(self):
        file_path = self.pdf_path
        if file_path:
            # Check if the file actually exists on the system
            if os.path.exists(file_path):
                # Create a QUrl from the local file path
                pdf_url = QUrl.fromLocalFile(file_path)

                # Use QDesktopServices to open the URL with the system's default application
                if QDesktopServices.openUrl(pdf_url):
                    print(f"Successfully opened: {file_path}")
                else:
                    QMessageBox.warning(
                        self,
                        "Error",
                        f"Could not open the file: {file_path}\n"
                        "Please ensure you have a default application set for PDF files."
                    )
                    print(f"Failed to open: {file_path}")
            else:
                QMessageBox.warning(
                    self,
                    "Error",
                    f"File not found at specified path: {file_path}\n"
                    "Please ensure the PDF file exists at this location."
                )
                print(f"File not found at specified path: {file_path}")
        else:
            QMessageBox.critical(
                self,
                "Configuration Error",
                "No PDF file path has been specified in the application."
            )
            print("No PDF file path has been specified.")


    def go_to_summary(self):
        if self.summary_window is None: # Only create once if you want a singleton-like behavior
            self.summary_window = SummaryPage(self.id)
        self.summary_window.show()
                                    
class MainMenu(QMainWindow):
    def __init__(self, conn):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("CV Reader")
        self.conn = conn

        print("Loading PDF data...")
        start_time = time.time()
        self.pdf_data = load_pdf(self.conn)
        print(f"{len(self.pdf_data)} PDF data loaded in {time.time() - start_time:.4f} seconds\n")

        # If no data loaded, show error and exit
        if not self.pdf_data:
            print("No PDF data found. Please load PDF files into the database.")
            QApplication.quit()
            return
        
        self.ui.searchButton.clicked.connect(self.get_search_result)

    def get_search_result(self):
        keywords = re.split(r",\s*", self.ui.keywordSearch.toPlainText())
        if self.ui.radioBM.isChecked():
            mode = "BM"
        elif self.ui.radioAC.isChecked():
            mode = "AC"
        else:
            mode = "KMP"
        result_amount = self.ui.topMatchesNumber.value()

        # Exact search
        print(f"Searching for keywords: {keywords} using {mode} algorithm")
        start_time = time.time()
        results = self.search(keywords, mode)
        exact_search_time = time.time() - start_time
        print(f"Exact search completed in {exact_search_time:.4f} seconds\n")

        # Fuzzy search
        print(f"Fuzzy searching for keywords: {keywords}")
        start_time = time.time()
        results = self.search(keywords, "Fuzzy", exact_result=results)
        fuzzy_search_time = time.time() - start_time
        print(f"Fuzzy search completed in {fuzzy_search_time:.4f} seconds\n")
        results = self.search(keywords, mode, result_amount)
        search_time = time.time() - start_time
        print(f"Search completed in {search_time:.4f} seconds")

        # Remove (0, *) entries from keywords
        for result in results:
            result['keywords'] = {kw: count for kw, count in result['keywords'].items() if count[0] > 0}

        # Sort by total matches, descending, and take top N
        results.sort(key=lambda x: x['total'], reverse=True)
        results = results[:result_amount]

        print(f"Top {min(result_amount, len(results))} results:")
        for result in results:
            print(f"Detail ID: {result['detail_id']}\nApplicant: {result['applicant_name']}\nTotal Matches: {result['total']}")
            for kw, (count, is_fuzzy) in result['keywords'].items():
                match_type = "Fuzzy" if is_fuzzy else "Exact"
                print(f"  {kw}: {count} ({match_type})")
            print()


        self.display_result(results, search_time)

    def display_result(self, results, search_time):
        self.clear_grid_layout()

        self.ui.searchResultData.setText(f"Search time: {search_time:.3f} s")
        for i, result in enumerate(results):
            applicant_id = result.get('detail_id')
            name = result.get('applicant_name')
            matches_number = result.get('total')
            matched_keywords = ""
            keywords_dict = result.get('keywords')
            for j, (key, value) in enumerate(keywords_dict.items()):
                matched_keywords += f"{j+1}. {key} : {value[0]} {"occurences" if value[0] > 1 else "occurence"}\n"

            result_card = ResultCard(applicant_id, name, matches_number, matched_keywords)
            row = i//3
            col = i%3
            self.ui.gridLayout.addWidget(result_card, row, col, Qt.AlignTop | Qt.AlignHCenter)

        self.ui.gridLayout.setRowStretch(self.ui.gridLayout.rowCount(), 1) # Add a stretch row at the bottom
        self.ui.gridLayout.setColumnStretch(self.ui.gridLayout.columnCount(), 1)

    def clear_grid_layout(self):
        """
        Clears all widgets from a QGridLayout.
        Ensures proper deletion of widgets to prevent memory leaks.
        """
        if self.ui.gridLayout is None:
            return

        # Iterate backwards to safely remove items.
        # Alternatively, you can always takeAt(0) repeatedly as shown in the previous answer.
        # Looping backward is generally more intuitive for lists where indices change.
        # For QLayouts, takeAt(0) is often used because it simplifies index management.

        # Method 1: Using takeAt(0) repeatedly (most common for QLayouts)
        while self.ui.gridLayout.count() > 0:
            item = self.ui.gridLayout.takeAt(0)
            if item.widget():
                widget = item.widget()
                widget.setParent(None) # Unparent the widget
                widget.deleteLater()   # Schedule for deletion
            del item # Delete the QLayoutItem itself

    def search(self, keywords, mode, exact_result=None):
        """
        Searches for keywords in the loaded PDF data using the specified algorithm.

        Args:
            keywords (list of str): List of keywords to search for.
            mode (str): Search algorithm ("KMP", "BM", "AC", "Fuzzy").
            result_amount (int): Number of top results to return.

        Returns:
            list: [
                {
                    'detail_id': int,
                    'applicant_name': str,
                    'keywords': {keyword: (occurrence, isFuzzy), ...},
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

                kw_counts = {kw: (len(ac_result.get(kw.lower(), [])), False) for kw in keywords}
                total = sum(count for count, _ in kw_counts.values())

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

        elif mode in ["KMP", "BM"]:
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
                    kw_counts[kw] = (count, False)
                total = sum(count for count, _ in kw_counts.values())

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

        else:  # Fuzzy search
            if exact_result is not None:
                results = exact_result.copy()
                # Create a mapping of detail_id to existing results for quick lookup
                existing_results = {result['detail_id']: result for result in results}
            else:
                existing_results = {}

            for detail_id, data in self.pdf_data.items():
                text = data['pattern_match']
                
                # Get existing keyword counts for this detail_id (if any)
                if detail_id in existing_results:
                    existing_kw_counts = existing_results[detail_id]['keywords']
                    # Skip keywords that already have >0 occurrences
                    keywords_to_search = [kw for kw in keywords if existing_kw_counts.get(kw, (0, False))[0] == 0]
                else:
                    keywords_to_search = keywords
                    existing_kw_counts = {}

                if not keywords_to_search:
                    continue

                fuzzy_kw_counts = {}
                for kw in keywords_to_search:
                    try:
                        count = fuzzy_search(text, kw.lower())
                        fuzzy_kw_counts[kw] = (count, True)
                    except Exception as e:
                        print(f"Error fuzzy searching for keyword '{kw}' in detail_id {detail_id}: {e}")
                        fuzzy_kw_counts[kw] = (0, True)

                fuzzy_total = sum(count for count, _ in fuzzy_kw_counts.values())

                if detail_id in existing_results:
                    # Update existing result with fuzzy matches
                    existing_result = existing_results[detail_id]
                    existing_result['keywords'].update(fuzzy_kw_counts)
                    existing_result['total'] += fuzzy_total
                elif fuzzy_total > 0:
                    cursor.execute(
                        "SELECT first_name, last_name FROM ApplicationDetail NATURAL JOIN ApplicantProfile WHERE detail_id = %s",
                        (detail_id,)
                    )
                    applicant = cursor.fetchone()
                    applicant_name = f"{applicant[0]} {applicant[1]}" if applicant else "Unknown"
                    
                    # Include all keywords with their counts (0 for non-fuzzy matched ones)
                    all_kw_counts = {kw: fuzzy_kw_counts.get(kw, (0, True)) for kw in keywords}
                    
                    results.append({
                        'detail_id': detail_id,
                        'applicant_name': applicant_name,
                        'keywords': all_kw_counts,
                        'total': fuzzy_total
                    })

        cursor.close()

        if results:
            for result in results: print(result)
        return results