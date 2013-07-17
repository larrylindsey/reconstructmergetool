#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from PySide import QtGui
import reconstructmergetool as rmt
# To do: Resize image, show right location, draw contour
#        Proper feedback when clicking buttons

class RmtGui(QtGui.QWidget):
    
    def __init__(self, c1, c2, img):
        super(RmtGui, self).__init__()
        
        self.initUI(c1,c2,img)
        
    def initUI(self,c1,c2,img):
        w,h = 750,500 # width and height of main window
        QtGui.QToolTip.setFont(QtGui.QFont('SansSerif', 10))
        self.setGeometry(100, 100, w, h) # ( startloc, dimensions )
        self.setWindowTitle('RECONSTRUCT MERGETOOL CONFLICT RESOLUTION') 
        
        # Left/Right Merge Button
        btn = QtGui.QPushButton('Contour 1', self)
        btn.setToolTip( str(c1) )
        btn.resize(btn.sizeHint())
        print(btn.size())
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
        
        # Turn img path into actual QImage object
        pic = QtGui.QImage()
        pic.load(img)
        pic = pic.copy() # Don't overwrite original

        # Load image into QLabel and modify size/position etc
        picbox1 = QtGui.QLabel(self)
        picbox1.setFrameStyle(QtGui.QFrame.Panel | QtGui.QFrame.Sunken)
        picbox1.setPixmap( QtGui.QPixmap.fromImage(pic) )
        picbox1.resize(300,300)
        picbox1.move(50,50)
        picbox1.setToolTip( str(c1) )
        
        picbox2 = QtGui.QLabel(self)
        picbox2.setFrameStyle(QtGui.QFrame.Panel | QtGui.QFrame.Sunken)
        picbox2.setPixmap( QtGui.QPixmap.fromImage(pic) )
        picbox2.resize(300,300)
        picbox2.move(w-50-300,50)
        picbox2.setToolTip( str(c2) )
        
        self.show()

        
def main():
    app = QtGui.QApplication(sys.argv)
    
    # === test contours
    a = rmt.getSeries('/home/michaelm/Documents/TestVolume/TVJ/Volumejosef.ser')
    c1 = a.sections[100].contours[5] #===
    c2 = a.sections[100].contours[6] #===
    img = '/home/michaelm/Documents/TestVolume/TVJ/'+a.sections[100].imgs[0].src
    # ==============
    
    win = RmtGui(c1,c2,img)
    sys.exit( app.exec_() )

if __name__ == '__main__':
    main()