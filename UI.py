# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(800, 600)
        MainWindow.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.price_box = QtGui.QTextEdit(self.centralwidget)
        self.price_box.setGeometry(QtCore.QRect(230, 70, 104, 87))
        self.price_box.setObjectName(_fromUtf8("price_box"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(140, 100, 72, 15))
        self.label.setObjectName(_fromUtf8("label"))
        self.tax_rate = QtGui.QSpinBox(self.centralwidget)
        self.tax_rate.setGeometry(QtCore.QRect(250, 250, 50, 22))
        self.tax_rate.setProperty("value", 20)
        self.tax_rate.setObjectName(_fromUtf8("tax_rate"))
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(150, 250, 72, 15))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.cal_tax_button = QtGui.QPushButton(self.centralwidget)
        self.cal_tax_button.setGeometry(QtCore.QRect(480, 180, 131, 31))
        self.cal_tax_button.setObjectName(_fromUtf8("cal_tax_button"))
        self.results_window = QtGui.QTextEdit(self.centralwidget)
        self.results_window.setGeometry(QtCore.QRect(370, 390, 104, 87))
        self.results_window.setObjectName(_fromUtf8("results_window"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setObjectName(_fromUtf8("menuHelp"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.cal_tax_button, QtCore.SIGNAL(_fromUtf8("clicked()")), MainWindow.button_On_Click)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.label.setText(_translate("MainWindow", "Price", None))
        self.label_2.setText(_translate("MainWindow", "Tax Rate", None))
        self.cal_tax_button.setText(_translate("MainWindow", "Calculate Tax", None))
        self.menuHelp.setTitle(_translate("MainWindow", "Help", None))

    def button_On_Click(self):
        price = self.price_box.toPlainText()
        rate  = self.tax_rate.value()
        tax_rate = int(price) * rate
        self.results_window.setText(str(tax_rate))

