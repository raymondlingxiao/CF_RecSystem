from PyQt4.QtGui import *
from PyQt4.QtCore import *
import UI
import sys

class uitest(QMainWindow,UI.Ui_MainWindow):
    def __init__(self, parent=None):
        super(uitest, self).__init__(parent)
        self.setupUi(self)

app = QApplication(sys.argv)
w = uitest()
w.show()
app.exec_()