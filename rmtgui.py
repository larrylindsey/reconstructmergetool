#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from PySide.QtCore import *
from PySide.QtGui import *
import reconstructmergetool as rmt
# To do: Resize image, show right location, draw contour
#        Proper feedback when clicking buttons
app = QApplication

class RmtGui(QtGui.QMainWindow):
    
    def __init__(self):
        super(RmtGui, self).__init__()
        self.startUI()
#         self.series1, self.series2 = self.seriesSelect()
        

    def startUI(self):
        w,h = 750,500 # width and height
        self.resize(w, h) # Starting location and dimensions of main container
        self.center()
        self.setWindowTitle('RECONSTRUCT MERGETOOL v.1') 
        
        # Quit button
        qbtn = QtGui.QPushButton('Quit', self)
        qbtn.clicked.connect(QtCore.QCoreApplication.instance().quit)
        qbtn.resize(qbtn.sizeHint())
        qbtn.move(0,h-qbtn.height()) # bottom left corner
        
        # Start button
        sbtn = QtGui.QPushButton('Begin Merge', self)
        sbtn.clicked.connect(self.beginMerge)
        sbtn.resize(sbtn.sizeHint())
        sbtn.move((w/2)-(sbtn.width()/2),h/2)
        
        # Series 1 load
        self.ser1path = None
        ser1btn = QtGui.QPushButton('Load Series 1', self)
        self.ser1path = ser1btn.clicked.connect(self.loadSeries)
        ser1btn.resize(ser1btn.sizeHint())
        ser1btn.move((w/2)-(ser1btn.width()*2), h/3)
        
        # Series 2 load
        self.ser2path = None
        ser2btn = QtGui.QPushButton('Load Series 2', self)
        self.ser2path = ser2btn.clicked.connect(self.loadSeries)
        ser2btn.resize(ser2btn.sizeHint())
        ser2btn.move((w/2)+(ser2btn.width()), h/3)
        
        
        
        
        
#         menubar = self.menuBar()
#         fileTab = menubar.addMenu('&File')

# QtGui.QHBoxLayout and QtGui.QVBoxLayout
#    - Box layout
        
        self.show()
        
    def beginMerge(self):
        if self.ser1path != None and self.ser2path != None:
            print('Go')
        else:
            print('Make sure you have loaded both series')

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