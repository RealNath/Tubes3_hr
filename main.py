import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow
from src.generated.main_menu_ui import Ui_MainWindow

class MenuWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        # Setup UI from generated file
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.setWindowTitle("CV Reader")
        self.setup_connections()
    
    def setup_connections(self):
        # Connect buttons using self.ui.button_name
        # self.ui.pushButton_start.clicked.connect(self.start_game)
        pass

def main():
    #!Harus pake ini
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    #!
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    menu_window = MenuWindow()
    menu_window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()