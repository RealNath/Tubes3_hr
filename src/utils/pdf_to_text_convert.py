import fitz  # PyMuPDF
import re

def extract_text(pdf_path):
    """
    Ekstrak semua teks dari file PDF menggunakan PyMuPDF.
    """
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

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

def convert_pdf_to_txt(pdf_path, regex_txt_path, pattern_txt_path, silent=True):
    """
    Konversi PDF ke dua file txt: satu untuk regex, satu untuk pattern matching.

    Args:
        pdf_path (str): File path input (PDF)
        regex_txt_path (str): Output path untuk hasil regex
        pattern_txt_path (str): Output path untuk hasil pattern matching
        silent (bool): Jika False, print pesan sukses
    """
    try:
        text = extract_text(pdf_path)
        ascii_text = text.encode('ascii', 'ignore').decode('ascii')

        # Untuk regex
        regex_text = re.sub(r' +', ' ', ascii_text)
        regex_text = re.sub(r'[\f]+', '', regex_text)
        regex_text = regex_text.strip()
        with open(regex_txt_path, 'w', encoding='utf-8') as f:
            f.write(regex_text)

        # Untuk pattern matching
        pattern_text = re.sub(r'[\r\n\f]+', ' ', ascii_text.lower())
        pattern_text = re.sub(r' +', ' ', pattern_text).strip()
        pattern_text = re.sub(r"[\/&']", "", pattern_text)
        with open(pattern_txt_path, 'w', encoding='utf-8') as f:
            f.write(pattern_text)

        if not silent:
            print(f"Successfully converted '{pdf_path}' to '{regex_txt_path}' (regex) and '{pattern_txt_path}' (pattern matching)")
    except Exception as e:
        print(f"An error occurred: {e}")