import sys
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5 import QtGui
from mainGUIFile import Ui_Dialog

class mainFile(QDialog):
    def __init__(self):
        super(mainFile, self).__init__()
        print("Setting Up Gui")
        self.firstUI = Ui_Dialog()
        self.firstUI.setupUi(self)
        
        self.firstUI.movie = QtGui.QMovie("../GUI MATERIAL/B.G/Black_Template.jpg")  # Corrected file path
        self.firstUI.label.setMovie(self.firstUI.movie)  # Corrected widget name
        self.firstUI.movie.start()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = mainFile()
    ui.show()
    sys.exit(app.exec_())
