#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from PySide import QtCore, QtGui
import reconstructmergetool as rmt

# To do: Resize image, show right location, draw contour
#        Proper feedback when clicking buttons

class RmtGui(QtGui.QMainWindow):
    
    def __init__(self):
        super(RmtGui, self).__init__()
        self.startUI()
        
    def startUI(self):
        # FRAME
        self.frame = QtGui.QFrame()
        self.frame.setGeometry(QtCore.QRect(10, 10, 561, 421))
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName("frame")

        # LAYOUT
        self.horizontalLayoutWidget = QtGui.QWidget(self.frame)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(59, 90, 441, 80))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        
        # LOAD SERIES 1
        self.ser1Button = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.ser1Button.setObjectName("ser1Button")
        self.horizontalLayout.addWidget(self.ser1Button)
        self.ser1Button.setText(QtGui.QApplication.translate("Form", "Load Series 1", None, QtGui.QApplication.UnicodeUTF8))
        self.ser1path = self.ser1Button.clicked.connect(self.loadSeries)
        
        # LOAD SERIES 2
        self.ser2Button = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.ser2Button.setObjectName("ser2Button")
        self.horizontalLayout.addWidget(self.ser2Button)
        self.ser2Button.setText(QtGui.QApplication.translate("Form", "Load Series 2", None, QtGui.QApplication.UnicodeUTF8))
        self.ser2path = self.ser2Button.clicked.connect(self.loadSeries)
        
        # QUIT
        self.quitButton = QtGui.QPushButton(self.frame)
        self.quitButton.setGeometry(QtCore.QRect(460, 390, 96, 27))
        self.quitButton.setObjectName("quitButton")
        self.quitButton.clicked.connect(QtCore.QCoreApplication.instance().quit)
        self.quitButton.setText(QtGui.QApplication.translate("Form", "Quit :(", None, QtGui.QApplication.UnicodeUTF8))
        
        # START BUTTON
        self.startButton = QtGui.QPushButton(self.frame)
        self.startButton.setGeometry(QtCore.QRect(200, 250, 161, 91))
        self.startButton.setObjectName("startButton")
        self.startButton.clicked.connect(self.beginMerge)
        self.startButton.setText(QtGui.QApplication.translate("Form", "START MERGE", None, QtGui.QApplication.UnicodeUTF8))
        
        self.frame.show()
        
    def beginMerge(self): #=== self.ser1path/ser2path are not None. what are they before file dialog?
        if self.ser1path == None and self.ser2path == None:
            print('Make sure you have loaded both series')
        else:
            print('Go')
                   
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
    
    def center(self):
        '''Center a window'''
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
    def contConf(self,c1,c2,img):
        # Left/Right Merge Button
        btn = QtGui.QPushButton('Contour 1', self)
        btn.setToolTip( str(c1) )
        btn.resize(btn.sizeHint())
        btn.move( 200-(85/2), h-(h/2)+150 ) # how far from topleft corner (x, y)
        
        btn2 = QtGui.QPushButton('Contour 2', self)
        btn2.setToolTip( str(c2) )
        btn2.resize(btn2.sizeHint())
        btn2.move( 550-(85/2) , h-(h/2)+150 ) 
        
        # Center merge button
        btn3 = QtGui.QPushButton('Output both', self)
        btn3.setToolTip('Click to output both options')
        btn3.resize(btn3.sizeHint())
        btn3.move( (w/2)-(btn3.width()/2), h-(h/2)+200 )
        
        # Show image/traces
        self.picbox(300,300,50,50,c1,img)
        self.picbox(300,300, w-350, 50,c2,img)
    
        
        
    def picbox(self, w, h, x, y,c,img):
        '''w = width of main window
           h = height of main window
           x = position in x direction, of picbox, from origin
           y = position in y direction, of picbox, from origin
           c = contour object for tooltip data
           img = path to image being shown in picbox'''
        # Turn img path into actual QImage object
        pic = QtGui.QImage()
        pic.load(img)
        pic = pic.copy() # Don't overwrite original
        # Load image into QLabel
        picbox = QtGui.QLabel(self)
        picbox.setFrameStyle(QtGui.QFrame.Panel)
        picbox.setPixmap( QtGui.QPixmap.fromImage(pic) )
        picbox.resize(w,h)
        picbox.move(x,y)
        picbox.setToolTip( str(c) )
        
def main():
    app = QtGui.QApplication(sys.argv)
    win = RmtGui()
    sys.exit( app.exec_() )

if __name__ == '__main__':
    main()