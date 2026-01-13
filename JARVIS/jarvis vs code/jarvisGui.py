
from jarvis import Ui_JarvisUI
from PyQt5 import QtCore , QtGui ,QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import QMovie
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt , QTimer , QTime , QDate
from PyQt5.uic import loadUiType
import Main
import os
import webbrowser as web
import sys
 
# ... (previous imports)

class MainThread(QThread):
    def __init__(self):
        super(MainThread, self).__init__()

    def run(self):
        Main.Task_Gui()

# ...

class Gui_Start(QMainWindow):
    def __init__(self):
        super().__init__()

        self.gui = Ui_JarvisUI()
        self.gui.setupUi(self)

        self.gui.pushButton_start.clicked.connect(self.startTask)  # Corrected button name
        self.gui.pushButton_exit.clicked.connect(self.close)
        self.gui.pushButton_chrome.clicked.connect(self.chrome_app)
        self.gui.pushButton_whatsapp.clicked.connect(self.whatsapp_app)
        self.gui.pushButton_yt.clicked.connect(self.yt_app)

        self.startExe = MainThread()
        self.startExe.start()
        
    # ... (rest of the methods)
 
        
def main():
    app = QApplication(sys.argv)
    jarvis_gui = Gui_Start()
    jarvis_gui.show()

    # Start the MainThread
 

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
  
            
        