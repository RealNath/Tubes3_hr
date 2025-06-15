import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow
from src.views.main_menu import MainMenu
from src.models.ApplicantProfile import *
from src.controller.MainController import *
import pymysql
from dotenv import load_dotenv

def main():
    #!Harus pake ini
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    #!
    
    # Load environment variables from .env
    load_dotenv()
    mysql_config = {
        'host': os.environ.get('MYSQL_HOST', 'localhost'),
        'user': os.environ.get('MYSQL_USER', 'root'),
        'password': os.environ.get('MYSQL_PASSWORD', ''),
        'database': os.environ.get('MYSQL_DB', 'cv_database')
    }

    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    # Create a global MySQL connection
    db_conn = pymysql.connect(**mysql_config)
    model = ApplicantProfileModel()
    menu_window = MainMenu(db_conn) #View
    coontroller = MainController(model, menu_window)
    menu_window.show()
    exit_code = app.exec_()
    db_conn.close()
    sys.exit(exit_code)

if __name__ == '__main__':
    main()