#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from PySide import QtGui
import reconstructmergetool as rmt

class rmtGui(QtGui.QWidget):
    
    def __init__(self, c1, c2):
        super(rmtGui, self).__init__()
        
        self.initUI(c1,c2)
        
    def initUI(self,c1,c2):
        w,h = 750,750 # width and height of main window
        QtGui.QToolTip.setFont(QtGui.QFont('SansSerif', 10))
        
        self.setToolTip('setToolTip')
        
        # Left/Right Merge Button
        btn = QtGui.QPushButton('Contour 1', self)
        btn.setToolTip( str(c1) )
        btn.resize(btn.sizeHint())
        btn.move( w/6 , h-(h/2)+50 ) # how far from topleft corner (x, y)
        
        btn2 = QtGui.QPushButton('Contour 2', self)
        btn2.setToolTip( str(c2) )
        btn2.resize(btn2.sizeHint())
        btn2.move( w-(w/6)-btn2.sizeHint().width() , h-(h/2)+50 ) 
        
        # Center merge button
        btn3 = QtGui.QPushButton('Output both', self)
        btn3.setToolTip('Click to output both options')
        btn3.resize(btn3.sizeHint())
        btn3.move( (w/2)-(btn3.width()/2), h-(h/2)+100 )
        
        # Contour displays
            # Displays portion of image containing the trace, draws trace on top of image
            # QWidget-> QFrame-> QLabel
        
        self.setGeometry(100, 100, w, h) # ( startloc, dimensions )
        self.setWindowTitle('RECONSTRUCT MERGETOOL CONFLICT RESOLUTION')    
        self.show()

        
def main():
    app = QtGui.QApplication(sys.argv)
    # === test contours
    a = rmt.getSeries('/home/michaelm/Documents/TestVolume/TVJ/Volumejosef.ser') #===
    c1 = a.sections[100].contours[5] #===
    c2 = a.sections[100].contours[6] #===
    # ==============
    win = rmtGui(c1,c2)
    sys.exit( app.exec_() )

if __name__ == '__main__':
    main()