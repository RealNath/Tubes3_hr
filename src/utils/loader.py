import re
import fitz  # PyMuPDF
import os

def load_pdf(conn):
    """
    Reads all CVs from MySQL database cv_database.ApplicationDetail,
    and returns a dict of the converted CVs.

    Args:
        conn: An existing MySQL connection

    Returns:
        dict: {
            detail_id: {
                'regex': str,
                'pattern_match': str
            }
        }
    """
    cursor = conn.cursor()
    cursor.execute("SELECT detail_id, cv_path FROM ApplicationDetail")
    rows = cursor.fetchall()
    result = {}
    for detail_id, cv_path in rows:
        if not cv_path or not os.path.isfile(cv_path):
            continue
        try:
            text = ""
            with fitz.open(cv_path) as doc:
                for page in doc:
                    text += page.get_text()

            # For regex
            text = text.encode('ascii', 'ignore').decode('ascii')
            regex = re.sub(r' +', ' ', text)
            regex = re.sub(r'[\f]+', '', regex)
            regex = regex.strip()

            # For pattern match
            pattern_match = re.sub(r'[\r\n\f]+', ' ', text.lower())
            pattern_match = re.sub(r' +', ' ', pattern_match).strip()
            pattern_match = re.sub(r"[\/&']", "", pattern_match)

            # Store both texts in a dict for each detail_id
            result[detail_id] = {
                'regex': regex,
                'pattern_match': pattern_match
            }
        except Exception as e:
            print(f"Error processing {cv_path} for detail_id {detail_id}: {e}")
            continue
    cursor.close()
    return result