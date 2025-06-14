import re
import fitz  # PyMuPDF
import os
from multiprocessing import Pool, cpu_count

def _process_pdf(args):
    detail_id, cv_path = args
    if not cv_path or not os.path.isfile(cv_path):
        print(f"Invalid path for detail_id {detail_id}: {cv_path}")
        return (detail_id, None)
    try:
        text = ""
        with fitz.open(cv_path) as doc:
            for page in doc:
                text += page.get_text()

        # For regex
        text_ascii = text.encode('ascii', 'ignore').decode('ascii')
        regex = re.sub(r' +', ' ', text_ascii)
        regex = re.sub(r'[\f]+', '', regex)
        regex = regex.strip()

        # For pattern match
        pattern_match = re.sub(r'[\r\n\f]+', ' ', text.lower())
        pattern_match = re.sub(r' +', ' ', pattern_match).strip()
        pattern_match = re.sub(r"[\/&']", "", pattern_match)

        return (detail_id, {
            'regex': regex,
            'pattern_match': pattern_match
        })
    except Exception as e:
        print(f"Error processing {cv_path} for detail_id {detail_id}: {e}")
        return (detail_id, None)

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
    cursor.close()

    with Pool(processes=cpu_count()) as pool:
        results = pool.map(_process_pdf, rows)

    result = {detail_id: data for detail_id, data in results if data is not None}
    return result