from pdfminer.high_level import extract_text
import re

def convert_for_regex(pdf_path, txt_path, silent=True):
    """
    Konversi PDF ke txt untuk regex.

    Args:
        pdf_path (str): File path input (PDF)
        txt_path (str): FIle path output (TXT).
    """
    try:
        text = extract_text(pdf_path)
        text = text.encode('ascii', 'ignore').decode('ascii')
        text = re.sub(r' +', ' ', text)
        text = re.sub(r'[\f]+', '', text)
        text = text.strip()
        with open(txt_path, 'w', encoding='utf-8') as txt_file:
            txt_file.write(text)
        if not silent:
            print(f"Successfully converted '{pdf_path}' to '{txt_path}'")
    except Exception as e:
        print(f"An error occurred: {e}")

def convert_for_pattern_matching(pdf_path, txt_path, silent=True):
    """
    Konversi PDF ke txt untuk pattern matching

    Args:
        pdf_path (str): File path input (PDF)
        txt_path (str): FIle path output (TXT).
    """
    try:
        text = extract_text(pdf_path)
        text = text.encode('ascii', 'ignore').decode('ascii')
        # hapus whitespace
        single_line_text = re.sub(r'[\r\n\f]+', ' ', text.lower())
        single_line_text = re.sub(r' +', ' ', single_line_text).strip()
        single_line_text = re.sub(r"[\/&']", "", single_line_text)

        with open(txt_path, 'w', encoding='utf-8') as txt_file:
            txt_file.write(single_line_text)
        if not silent:
            print(f"Successfully converted '{pdf_path}' to a single line in '{txt_path}'")
    except Exception as e:
        print(f"An error occurred: {e}")