import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow
from src.views.main_menu import MainMenu

def main():
    #!Harus pake ini
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    #!
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    menu_window = MainMenu()
    menu_window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()