# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qtrmtui.ui'
#
# Created: Tue Jul 23 15:05:02 2013
#      by: pyside-uic 0.2.14 running on PySide 1.1.2
#
# WARNING! All changes made in this file will be lost!

# Last update: 7/23/2013
# Changed Ui_Form(object) to Ui_Form(QtGui.QMainWindow) so that self.show() works
import sys
from PySide import QtCore, QtGui


class Ui_Form(QtGui.QMainWindow):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(579, 441)
        
        # Layout
        self.horizontalLayoutWidget = QtGui.QWidget(Form)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(69, 140, 441, 80))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        
        # Load series 1 button
        self.pushButton = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.pushButton.setObjectName("pushButton")
        self.ser1path = self.pushButton.clicked.connect(self.loadSeries)
        self.horizontalLayout.addWidget(self.pushButton)
        
        # Load series 2 button
        self.pushButton_2 = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.ser2path = self.pushButton_2.clicked.connect(self.loadSeries)
        self.horizontalLayout.addWidget(self.pushButton_2)
        
        # Start merge button
        self.pushButton_3 = QtGui.QPushButton(Form)
        self.pushButton_3.setGeometry(QtCore.QRect(210, 300, 161, 91))
        self.pushButton_3.setObjectName("pushButton_3")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        
    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_3.setText(QtGui.QApplication.translate("Form", "START MERGE", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("Form", "Load Series 1", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_2.setText(QtGui.QApplication.translate("Form", "Load Series 2", None, QtGui.QApplication.UnicodeUTF8))
    
    def loadSeries(self):
        dialog = QtGui.QFileDialog(self)
        dialog.setFileMode(QtGui.QFileDialog.AnyFile)
        dialog.setNameFilter('Series files (*.ser)')
        dialog.setViewMode(QtGui.QFileDialog.Detail)
        if dialog.exec_():
            seriesPath = dialog.selectedFiles()
            return seriesPath
        else:
            return None
        
def main():
    app = QtGui.QApplication(sys.argv)
    win = Ui_Form()
    win.show()
    sys.exit( app.exec_() )
if __name__ == '__main__':
    main()