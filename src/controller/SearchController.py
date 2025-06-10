#from models.ApplicantProfile import *
from utils.pdf_to_text_convert import *
from utils.seeder import *
from views.main_menu import MainMenu
import re
import shutil
import os
import pathlib

def cv_search(keywords, mode, result_amount):
    clean_output_dir()
    convert_all_pdfs_to_pattern_match_txt()

def clean_output_dir():
    OUTPUT_FOLDER = "data/txt"
    if os.path.exists(OUTPUT_FOLDER):
    # Remove all files in the directory
        for filename in os.listdir(OUTPUT_FOLDER):
            file_path = os.path.join(OUTPUT_FOLDER, filename)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"Error deleting {file_path}: {e}")
    else:
        # Create the output folder if it doesn't exist
        os.makedirs(OUTPUT_FOLDER)

if __name__ == "__main__":
    cv_search("A", "A", 1)