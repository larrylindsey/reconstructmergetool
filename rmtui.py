# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qtrmtui.ui'
#
# Created: Wed Jul 24 11:58:26 2013
#      by: pyside-uic 0.2.14 running on PySide 1.1.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(579, 440)
        
        # FRAME
        self.frame = QtGui.QFrame(Form)
        self.frame.setGeometry(QtCore.QRect(10, 10, 561, 421))
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName("frame")

        # LAYOUT
        self.horizontalLayoutWidget = QtGui.QWidget(self.frame)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(59, 90, 441, 80))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
    #     self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        
        # LOAD SERIES 1
        self.ser1Button = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.ser1Button.setObjectName("ser1Button")
        self.horizontalLayout.addWidget(self.ser1Button)
        
        # LOAD SERIES 2
        self.ser2Button = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.ser2Button.setObjectName("ser2Button")
        self.horizontalLayout.addWidget(self.ser2Button)
            
        # QUIT
        self.quitButton = QtGui.QPushButton(self.frame)
        self.quitButton.setGeometry(QtCore.QRect(460, 390, 96, 27))
        self.quitButton.setObjectName("quitButton")
        
        # START
        self.startButton = QtGui.QPushButton(self.frame)
        self.startButton.setGeometry(QtCore.QRect(200, 250, 161, 91))
        self.startButton.setObjectName("startButton")
    
        self.retranslateUi(Form)
        QtCore.QObject.connect(self.quitButton, QtCore.SIGNAL("clicked()"), Form.close)
        QtCore.QObject.connect(self.ser1Button, QtCore.QAbstract) #=== file dialog goes here
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.ser1Button.setText(QtGui.QApplication.translate("Form", "Load Series 1", None, QtGui.QApplication.UnicodeUTF8))
        self.ser2Button.setText(QtGui.QApplication.translate("Form", "Load Series 2", None, QtGui.QApplication.UnicodeUTF8))
        self.quitButton.setText(QtGui.QApplication.translate("Form", "Quit :(", None, QtGui.QApplication.UnicodeUTF8))
        self.startButton.setText(QtGui.QApplication.translate("Form", "START MERGE", None, QtGui.QApplication.UnicodeUTF8))

