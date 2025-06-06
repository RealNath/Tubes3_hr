from convertPDFtoText import convert_for_regex
import os
from concurrent.futures import ThreadPoolExecutor
import random
from faker import Faker
import sqlite3
import threading

# Config
DB_PATH = 'data/cv_database.db'
PDF_DIR = 'data/pdf'
TXT_DIR = 'data/txt'
PDF_TO_TXT_WORKERS = 32
INDONESIAN_PHONE_PREFIXES = [
    "0811", "0812", "0813", "0821", "0822", "0823", "0851", "0852", "0853",                         # Telkomsel
    "0814", "0815", "0816", "0855", "0856", "0857", "0858", "0895", "0896", "0897", "0898", "0899", # Indosat Ooredoo
    "0817", "0818", "0819", "0859", "0877", "0878",                                                 # XL Axiata
    "0831", "0832", "0833", "0838",                                                                 # AXIS
    "0881", "0882", "0883", "0884", "0885", "0886", "0887", "0888", "0889"                          # Smartfren
]

def convert_all_pdfs_to_txt():
    """
    Convert all PDF files in the DATA_PDF_DIR to TXT files in REGEX_TXT_DIR.
    """

    def convert_pdf_file(args):
        """
        Convert a single PDF file to TXT using convert_for_regex.
        Updates a shared counter and prints progress (thread-safe).
        """
        pdf_path, txt_path, total, counter, lock = args
        convert_for_regex(pdf_path, txt_path)
        with lock:
            counter[0] += 1
            print(f"[{counter[0]}/{total}] Converted {os.path.basename(pdf_path)}")

    if not os.path.exists(TXT_DIR):
        os.makedirs(TXT_DIR)

    pdf_files = [f for f in os.listdir(PDF_DIR) if f.endswith('.pdf')]
    total = len(pdf_files)

    if not total:
        print("No PDF files found in the data directory.")
        return

    counter = [0]
    lock = threading.Lock()
    tasks = [
        (
            os.path.join(PDF_DIR, filename),
            os.path.join(TXT_DIR, filename.replace('.pdf', '.txt')),
            total,
            counter,
            lock
        )
        for filename in pdf_files
    ]

    with ThreadPoolExecutor(max_workers=PDF_TO_TXT_WORKERS) as executor:
        executor.map(convert_pdf_file, tasks)

def generate_applicant(fake):
    """
    Generate a fake applicant profile using the Faker library and Indonesian phone prefixes.
    Returns: (first_name, last_name, dob, address, phone)
    """
    first_name = fake.first_name()
    last_name = fake.last_name()
    dob = fake.date_of_birth(minimum_age=18, maximum_age=65).isoformat()
    address = fake.address().replace('\n', ', ')
    phone_prefix = random.choice(INDONESIAN_PHONE_PREFIXES)
    phone = f"{phone_prefix}{random.randint(1, 99999999):8d}"
    return first_name, last_name, dob, address, phone

def seed_database():
    """
    Seed the SQLite database with applicant and application detail data.
    """    
    fake = Faker('id_ID')
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create tables if don't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ApplicantProfile (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT,
            last_name TEXT,
            date_of_birth TEXT,
            address TEXT,
            phone_number TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ApplicationDetail (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            applicant_id INTEGER,
            application_role TEXT,
            cv_path TEXT,
            FOREIGN KEY(applicant_id) REFERENCES ApplicantProfile(id)
        )
    ''')

    # Get all txt files
    os.makedirs(TXT_DIR, exist_ok=True)
    txt_files = [f for f in os.listdir(TXT_DIR) if f.endswith('.txt')]
    if not txt_files:
        print("No TXT files found. Converting PDFs to TXT...")
        convert_all_pdfs_to_txt()
        txt_files = [f for f in os.listdir(TXT_DIR) if f.endswith('.txt')]
    
    applicant_ids = []

    # Prepopulate with some applicants for possible reuse
    for _ in range(int(len(txt_files) * 0.3)):
        first_name, last_name, dob, address, phone = generate_applicant(fake)
        cursor.execute('''
            INSERT INTO ApplicantProfile (first_name, last_name, date_of_birth, address, phone_number)
            VALUES (?, ?, ?, ?, ?)
        ''', (first_name, last_name, dob, address, phone))
        applicant_ids.append(cursor.lastrowid)

    for txt_file in txt_files:
        # 30% chance to reuse an applicant, or always reuse if remaining applications == prepopulate_count
        remaining_applications = len(txt_files) - len(applicant_ids)
        if applicant_ids and random.random() < 0.3:
            applicant_id = random.choice(applicant_ids)
        else:
            first_name, last_name, dob, address, phone = generate_applicant(fake)
            cursor.execute('''
                INSERT INTO ApplicantProfile (first_name, last_name, date_of_birth, address, phone_number)
                VALUES (?, ?, ?, ?, ?)
            ''', (first_name, last_name, dob, address, phone))
            applicant_id = cursor.lastrowid
            applicant_ids.append(applicant_id)

        # Search for application_role in first or second line
        txt_path = os.path.join(TXT_DIR, txt_file)
        with open(txt_path, 'r', encoding='utf-8') as f:
            first_line = f.readline().strip()
            if len(first_line) <= 2:
                second_line = f.readline().strip()
                application_role = second_line
            else:
                application_role = first_line

        # Use the corresponding PDF file in the data folder, relative to project root
        pdf_filename = txt_file.replace('.txt', '.pdf')
        cv_path = os.path.join('data', pdf_filename)
        cursor.execute('''
            INSERT INTO ApplicationDetail (applicant_id, application_role, cv_path)
            VALUES (?, ?, ?)
        ''', (applicant_id, application_role, cv_path))

    # Clean up any unused applicants
    cursor.execute('''
        DELETE FROM ApplicantProfile
        WHERE id NOT IN (SELECT DISTINCT applicant_id FROM ApplicationDetail)
    ''')

    conn.commit()
    cursor.close()
    conn.close()
    print("Database seeded with applicants and application details.")

if __name__ == '__main__':
    import sys

    answer = input("Convert PDFs to TXT before seeding the database? (y/N): ").strip().lower()
    if answer == 'y':
        convert_all_pdfs_to_txt()
        print("All PDFs converted to TXT files.\n")
    elif answer not in ('n', ''):
        print("Unrecognized input, skipping PDF conversion.\n")

    answer = input("Drop existing database and seed new data? (Y/n): ").strip().lower()
    if answer == 'y' or answer == '':
        if os.path.exists(DB_PATH):
            os.remove(DB_PATH)
            print("Existing database dropped.")
        else:
            print("No existing database found, proceeding to seed new data.")
    elif answer != 'n':
        print("Unrecognized input, skipping database drop.\n")
    
    seed_database()