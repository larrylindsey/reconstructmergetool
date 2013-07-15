#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from PyQt4 import QtGui

class rmtGui(QtGui.QWidget):
    
    def __init__(self):
        super(rmtGui, self).__init__()
        
        self.initUI()
        
    def initUI(self):
        w,h = 750,750 # width and height of main window
        QtGui.QToolTip.setFont(QtGui.QFont('SansSerif', 10))
        
        self.setToolTip('RECONSTRUCT MERGETOOL')
        
        # Left/Right Merge Button
        btn = QtGui.QPushButton('MERGE 1', self)
        btn.setToolTip('Click to output this option')
        btn.resize(btn.sizeHint())
        btn.move( w/6 , h-(h/2)+50 ) # how far from topleft corner (x, y)
        
        btn2 = QtGui.QPushButton('MERGE 2', self)
        btn2.setToolTip('Contour attributes go here')
        btn2.resize(btn2.sizeHint())
        btn2.move( w-(w/6)-btn2.sizeHint().width() , h-(h/2)+50 ) 
        
        self.setGeometry(100, 100, w, h) # ( startloc, dimensions )
        self.setWindowTitle('Contour attributes go here')    
        self.show()

def main():
    app = QtGui.QApplication(sys.argv)
    win = rmtGui()
    sys.exit( app.exec_() )

if __name__ == '__main__':
    main()