from pdf_to_text_convert import convert_pdf_to_txt
import os
import random
from faker import Faker
import pymysql
from concurrent.futures import ProcessPoolExecutor
from tqdm import tqdm
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

DB_NAME = os.environ.get('MYSQL_DB', 'cv_database')
MYSQL_CONFIG = {
    'host': os.environ.get('MYSQL_HOST', 'localhost'),
    'user': os.environ.get('MYSQL_USER', 'root'),
    'password': os.environ.get('MYSQL_PASSWORD', ''),
    'database': DB_NAME
}

PDF_DIR = 'data/pdf'
REGEX_TXT_DIR = 'data/regex_txt'
PATTERN_MATCH_TXT_DIR = 'data/pattern_match_txt'
INDONESIAN_PHONE_PREFIXES = [
    "0811", "0812", "0813", "0821", "0822", "0823", "0851", "0852", "0853",                         # Telkomsel
    "0814", "0815", "0816", "0855", "0856", "0857", "0858", "0895", "0896", "0897", "0898", "0899", # Indosat Ooredoo
    "0817", "0818", "0819", "0859", "0877", "0878",                                                 # XL Axiata
    "0831", "0832", "0833", "0838",                                                                 # AXIS
    "0881", "0882", "0883", "0884", "0885", "0886", "0887", "0888", "0889"                          # Smartfren
]
roles = {"ACCOUNTANT":0, "ADVOCATE":0, "AGRICULTURE":0,
         "APPAREL":0, "ARTS":0, "AUTOMOBILE":0,
         "AVIATION":0, "BANKING":0, "BPO":0,
         "BUSINESS-DEVELOPMENT":0, "CHEF":0, "CONSTRUCTION":0,
         "CONSULTANT":0, "DESIGNER":0, "DIGITAL-MEDIA":0,
         "ENGINEERING":0, "FINANCE":0, "FITNESS":0,
         "HEALTHCARE":0, "HR":0, "INFORMATION-TECHNOLOGY":0,
         "PUBLIC-RELATIONS":0, "SALES":0, "TEACHER":0}

def get_mysql_connection(database=None):
    """
    Get a MySQL connection. If database is None, connect without selecting a DB.
    """
    config = MYSQL_CONFIG.copy()
    if database:
        config['database'] = database
    return pymysql.connect(**config)

def create_database_and_tables(conn):
    """
    Create the cv_database and required tables if they do not exist.
    """
    cursor = conn.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
    cursor.close()

    cursor = conn.cursor()
    cursor.execute(f"USE {DB_NAME}")
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ApplicantProfile(
            applicant_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
            first_name VARCHAR(50) DEFAULT NULL,
            last_name VARCHAR(50) DEFAULT NULL,
            date_of_birth DATE DEFAULT NULL,
            address VARCHAR(255) DEFAULT NULL,
            phone_number VARCHAR(20) DEFAULT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ApplicationDetail(
            detail_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
            applicant_id INT NOT NULL,
            application_role VARCHAR(100) DEFAULT NULL,
            cv_path TEXT,
            FOREIGN KEY (applicant_id) REFERENCES ApplicantProfile(applicant_id)
        )
    ''')
    cursor.close()

def convert_pdf_file(args):
    """
    Convert a single PDF file to TXT using convert_pdf_to_txt.
    """
    pdf_path, regex_txt_path, pattern_txt_path = args
    try:
        convert_pdf_to_txt(pdf_path, regex_txt_path, pattern_txt_path)
        return os.path.basename(pdf_path), True
    except Exception:
        return os.path.basename(pdf_path), False

def convert_all_pdfs_to_txt():
    """
    Convert all PDF files in the PDF_DIR to TXT files in REGEX_TXT_DIR and PATTERN_MATCH_TXT_DIR using parallel processing.
    """
    for dir_path in [REGEX_TXT_DIR, PATTERN_MATCH_TXT_DIR]:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

    pdf_files = [f for f in os.listdir(PDF_DIR) if f.endswith('.pdf')]
    total = len(pdf_files)

    if not total:
        print("No PDF files found in the data directory.")
        return

    tasks = [
        (
            os.path.join(PDF_DIR, filename),
            os.path.join(REGEX_TXT_DIR, filename.replace('.pdf', '.txt')),
            os.path.join(PATTERN_MATCH_TXT_DIR, filename.replace('.pdf', '.txt'))
        )
        for filename in pdf_files
    ]

    executor = None
    try:
        executor = ProcessPoolExecutor()
        with tqdm(total=total, unit=" file") as pbar:
            for filename, success in executor.map(convert_pdf_file, tasks):
                if not success:
                    print(f"Failed to convert {filename}")
                pbar.update(1)
    except KeyboardInterrupt:
        print("\nPDF conversion interrupted.")
        if executor:
            executor.shutdown(wait=False, cancel_futures=True)
        raise
    finally:
        if executor:
            executor.shutdown(wait=True)

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

def seed_database(conn):
    """
    Seed the MySQL database with applicant and application detail data.
    """
    
    fake = Faker('id_ID')
    create_database_and_tables(conn)
    cursor = conn.cursor()

    # Get all txt files from REGEX_TXT_DIR
    os.makedirs(REGEX_TXT_DIR, exist_ok=True)
    txt_files = [f for f in os.listdir(REGEX_TXT_DIR) if f.endswith('.txt')]
    if not txt_files:
        print("No TXT files found. Converting PDFs to TXT...")
        convert_all_pdfs_to_txt()
        txt_files = [f for f in os.listdir(REGEX_TXT_DIR) if f.endswith('.txt')]

    applicant_ids = []

    # Prepopulate with some applicants for possible reuse
    for _ in range(int(len(txt_files) * 0.3)):
        first_name, last_name, dob, address, phone = generate_applicant(fake)
        cursor.execute('''
            INSERT INTO ApplicantProfile (first_name, last_name, date_of_birth, address, phone_number)
            VALUES (%s, %s, %s, %s, %s)
        ''', (first_name, last_name, dob, address, phone))
        applicant_ids.append(cursor.lastrowid)

    for txt_file in txt_files:
        # 30% chance to reuse an applicant
        if applicant_ids and random.random() < 0.3:
            applicant_id = random.choice(applicant_ids)
        else:
            first_name, last_name, dob, address, phone = generate_applicant(fake)
            cursor.execute('''
                INSERT INTO ApplicantProfile (first_name, last_name, date_of_birth, address, phone_number)
                VALUES (%s, %s, %s, %s, %s)
            ''', (first_name, last_name, dob, address, phone))
            applicant_id = cursor.lastrowid
            applicant_ids.append(applicant_id)

        # Search for application_role in regex txt file
        txt_path = os.path.join(REGEX_TXT_DIR, txt_file)
        with open(txt_path, 'r', encoding='utf-8') as f:
            text = f.read()
            for role in roles:
                roles[role] = text.count(role)
            application_role = max(roles, key=roles.get)

        pdf_filename = txt_file.replace('.txt', '.pdf')
        cv_path = 'data/pdf/' + pdf_filename
        cursor.execute('''
            INSERT INTO ApplicationDetail (applicant_id, application_role, cv_path)
            VALUES (%s, %s, %s)
        ''', (applicant_id, application_role, cv_path))

    # Clean up any unused applicants
    cursor.execute('''
        DELETE FROM ApplicantProfile
        WHERE applicant_id NOT IN (SELECT DISTINCT applicant_id FROM ApplicationDetail)
    ''')

    conn.commit()
    cursor.close()
    print("Database seeded with applicants and application details.")

if __name__ == '__main__':
    conn = get_mysql_connection(DB_NAME)

    answer = input("Convert PDFs to TXT before seeding the database? (y/N): ").strip().lower()
    if answer == 'y':
        convert_all_pdfs_to_txt()
        print("All PDFs converted to TXT files.\n")
    elif answer not in ('n', ''):
        print("Unrecognized input, skipping PDF conversion.\n")


    answer = input("Drop existing database and seed new data? (Y/n): ").strip().lower()
    if answer == 'y' or answer == '':
        cursor = conn.cursor()
        cursor.execute(f"DROP DATABASE IF EXISTS {DB_NAME}")
        cursor.close()
        print("Existing database dropped.")
    elif answer != 'n':
        print("Unrecognized input, skipping database drop.\n")

    seed_database(conn)
    conn.close()