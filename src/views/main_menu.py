from src.generated.main_menu_ui import Ui_MainWindow
from src.utils.loader import load_pdf
from PyQt5.QtWidgets import QMainWindow, QApplication
import re
from src.utils.kmp_search import kmp_search
from src.utils.bm_search import bm_search
from src.utils.ac_search import ac_search
from src.utils.fuzzy_search import fuzzy_search
import time

class MainMenu(QMainWindow):
    def __init__(self, conn):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
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