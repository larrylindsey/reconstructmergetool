#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PySide import QtCore, QtGui
import reconstructmergetool as rmt

class mainFrame(QtGui.QFrame):
    '''This class is the main window of Reconstruct Mergetool. All other objects inherit this class
    such that they can be displayed within it.'''
    def __init__(self, parent=None):
        QtGui.QFrame.__init__(self, parent)
       
        self.setGeometry(100,100,800,600)
        
        # QUIT BUTTON. Always exists
        self.qButton = QtGui.QPushButton(self)
        self.qButton.setText('Quit')
        self.qButton.setGeometry(QtCore.QRect(704, 573, 96, 27))
        self.qButton.clicked.connect(QtCore.QCoreApplication.instance().quit)
        
        self.show()
        
class welcomeButton(QtGui.QPushButton):
    def __init__(self, parent=None):
        QtGui.QPushButton.__init__(self, parent)
    
        # WELCOME BUTTON
        self.setText('WELCOME TO RECONSTRUCT MERGETOOL\nClick to continue')
        self.setGeometry(200,200,400,100)
        self.clicked.connect(self.whenClicked)
        self.show()

    def whenClicked(self):
        '''Hides the welcomeButton and begins next frame'''
        self.hide()
        
        
class loadSeries(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        
        # Load ser 1
        
        # Load ser 2
        
    def browseFiles(self):
        dialog = QtGui.QFileDialog(self)
        dialog.setFileMode(QtGui.QFileDialog.AnyFile)
        dialog.setNameFilter('Series files (*.ser)')
        dialog.setViewMode(QtGui.QFileDialog.Detail)

def main():
    app = QtGui.QApplication(sys.argv)
    win = mainFrame()
    welcomeButton(win) # Begin of 'chain of frames' that are the different states of rmt
    sys.exit( app.exec_() )

if __name__ == '__main__':
    main()




# class loadWindow(QtGui.QWidget):
#     
#     def __init__(self, parent=None):
#         QtGui.QWidget.__init__(self, parent)
#         self.startUI()
#         
#     def startUI(self):
#         # FRAME
#         self.frame = QtGui.QFrame()
#         self.frame.setGeometry(QtCore.QRect(10, 10, 561, 421))
#         self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
#         self.frame.setFrameShadow(QtGui.QFrame.Raised)
#         self.frame.setObjectName("frame")
# 
#         # LAYOUT
#         self.horizontalLayoutWidget = QtGui.QWidget(self.frame)
#         self.horizontalLayoutWidget.setGeometry(QtCore.QRect(59, 90, 441, 80))
#         self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
#         self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
#         self.horizontalLayout.setObjectName("horizontalLayout")
#         
#         # LOAD SERIES 1
#         self.ser1Button = QtGui.QPushButton(self.horizontalLayoutWidget)
#         self.ser1Button.setObjectName("ser1Button")
#         self.horizontalLayout.addWidget(self.ser1Button)
#         self.ser1Button.setText(QtGui.QApplication.translate("Form", "Load Series 1", None, QtGui.QApplication.UnicodeUTF8))
# #         self.ser1path = self.ser1Button.clicked.connect(self.loadSeries)
#         print(self.ser1Button.clicked.connect(self.loadSeries))
#         
#         # LOAD SERIES 2
#         self.ser2Button = QtGui.QPushButton(self.horizontalLayoutWidget)
#         self.ser2Button.setObjectName("ser2Button")
#         self.horizontalLayout.addWidget(self.ser2Button)
#         self.ser2Button.setText(QtGui.QApplication.translate("Form", "Load Series 2", None, QtGui.QApplication.UnicodeUTF8))
# #         self.ser2path = self.ser2Button.clicked.connect(self.loadSeries)
#         print(self.ser2Button.clicked.connect(self.loadSeries))
#         
#         # QUIT
#         self.quitButton = QtGui.QPushButton(self.frame)
#         self.quitButton.setGeometry(QtCore.QRect(460, 390, 96, 27))
#         self.quitButton.setObjectName("quitButton")
#         self.quitButton.clicked.connect(QtCore.QCoreApplication.instance().quit)
#         self.quitButton.setText(QtGui.QApplication.translate("Form", "Quit", None, QtGui.QApplication.UnicodeUTF8))
#         
#         # START BUTTON
#         self.startButton = QtGui.QPushButton(self.frame)
#         self.startButton.setGeometry(QtCore.QRect(200, 250, 161, 91))
#         self.startButton.setObjectName("startButton")
#         self.startButton.clicked.connect(self.beginMerge)
#         self.startButton.setText(QtGui.QApplication.translate("Form", "START MERGE", None, QtGui.QApplication.UnicodeUTF8))
#         
#         self.frame.show()
#         
#     def beginMerge(self): #=== self.ser1path/ser2path are not None. what are they before file dialog?
#         if self.ser1path == None and self.ser2path == None:
#             print('Make sure you have loaded both series')
#         else:
#             print('Go')
#                    
#     def loadSeries(self):
#         dialog = QtGui.QFileDialog(self)
#         dialog.setFileMode(QtGui.QFileDialog.AnyFile)
#         dialog.setNameFilter('Series files (*.ser)')
#         dialog.setViewMode(QtGui.QFileDialog.Detail)
#         if dialog.exec_():
#             seriesPath = dialog.selectedFiles()
#             return seriesPath
#         else:
#             return None
# 
#     def picbox(self, w, h, x, y,c,img):
#         '''w = width of main window
#            h = height of main window
#            x = position in x direction, of picbox, from origin
#            y = position in y direction, of picbox, from origin
#            c = contour object for tooltip data
#            img = path to image being shown in picbox'''
#         # Turn img path into actual QImage object
#         pic = QtGui.QImage()
#         pic.load(img)
#         pic = pic.copy() # Don't overwrite original
#         # Load image into QLabel
#         picbox = QtGui.QLabel(self)
#         picbox.setFrameStyle(QtGui.QFrame.Panel)
#         picbox.setPixmap( QtGui.QPixmap.fromImage(pic) )
#         picbox.resize(w,h)
#         picbox.move(x,y)
#         picbox.setToolTip( str(c) )
# 
# class serAttWindow(QtGui.QWidget):   
#     def __init__(self, parent=None):
#         QtGui.QWidget.__init__(self, parent)
#         self.startUI()
#         
#     def startUI(self):
#         # FRAME
#         self.frame = QtGui.QFrame()
#         self.frame.setGeometry(QtCore.QRect(10, 10, 561, 421))
#         self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
#         self.frame.setFrameShadow(QtGui.QFrame.Raised)
#         self.frame.setObjectName("frame")
# 
#         # LAYOUT
#         self.horizontalLayoutWidget = QtGui.QWidget(self.frame)
#         self.horizontalLayoutWidget.setGeometry(QtCore.QRect(59, 90, 441, 80))
#         self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
#         self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
#         self.horizontalLayout.setObjectName("horizontalLayout")
#         
#         # LOAD SERIES 1
#         self.ser1Button = QtGui.QPushButton(self.horizontalLayoutWidget)
#         self.ser1Button.setObjectName("ser1Button")
#         self.horizontalLayout.addWidget(self.ser1Button)
#         self.ser1Button.setText(QtGui.QApplication.translate("Form", "Load Series 1", None, QtGui.QApplication.UnicodeUTF8))
#         self.ser1path = self.ser1Button.clicked.connect(self.loadSeries)
#         
#         # LOAD SERIES 2
#         self.ser2Button = QtGui.QPushButton(self.horizontalLayoutWidget)
#         self.ser2Button.setObjectName("ser2Button")
#         self.horizontalLayout.addWidget(self.ser2Button)
#         self.ser2Button.setText(QtGui.QApplication.translate("Form", "Load Series 2", None, QtGui.QApplication.UnicodeUTF8))
#         self.ser2path = self.ser2Button.clicked.connect(self.loadSeries)
#         
#         # QUIT
#         self.quitButton = QtGui.QPushButton(self.frame)
#         self.quitButton.setGeometry(QtCore.QRect(460, 390, 96, 27))
#         self.quitButton.setObjectName("quitButton")
#         self.quitButton.clicked.connect(QtCore.QCoreApplication.instance().quit)
#         self.quitButton.setText(QtGui.QApplication.translate("Form", "Quit :(", None, QtGui.QApplication.UnicodeUTF8))
#         
#         # START BUTTON
#         self.startButton = QtGui.QPushButton(self.frame)
#         self.startButton.setGeometry(QtCore.QRect(200, 250, 161, 91))
#         self.startButton.setObjectName("startButton")
#         self.startButton.clicked.connect(self.beginMerge)
#         self.startButton.setText(QtGui.QApplication.translate("Form", "START MERGE", None, QtGui.QApplication.UnicodeUTF8))
#         
#         self.frame.show()
#         
#         
# def main():
#     app = QtGui.QApplication(sys.argv)
#     win = loadWindow()
#     sys.exit( app.exec_() )
# 
# if __name__ == '__main__':
#     main()