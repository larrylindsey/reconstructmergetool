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
    
        self.show()
        
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