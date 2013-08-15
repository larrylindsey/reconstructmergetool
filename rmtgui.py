#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import reconstructmergetool as rmt
from PySide import QtCore, QtGui
import time
# Follows the same steps as reconstructmergetool.mergeSeries(etc) but doesnt call that function...
# ... easier to implement separately for GUI
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
        self.parent=parent
        # WELCOME BUTTON
        self.setText('WELCOME TO RECONSTRUCT MERGETOOL\nClick to continue')
        self.setGeometry(200,200,400,100)
        self.clicked.connect(self.whenClicked)
        self.show()

    def whenClicked(self):
        '''Hides the welcomeButton and begins next frame'''
        self.hide()
        loadSeries(self.parent)
        
class loadSeries(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.parent=parent
        # Frame
        self.frame = QtGui.QFrame(parent)
        self.frame.setGeometry(0,0,800,500)
        
        # Load ser 1
        self.s1Button = QtGui.QPushButton(self.frame)
        self.s1Button.setText('Load Series 1')
        self.s1Button.setGeometry(100,200,200,100)
        self.s1path = None # updated by browseFiles()
        self.s1Button.clicked.connect(self.browseFiles)
        
        # Load ser 2
        self.s2Button = QtGui.QPushButton(self.frame)
        self.s2Button.setText('Load Series 2')
        self.s2Button.setGeometry(500,200,200,100)
        self.s2path = None # updated by browseFiles2()
        self.s2Button.clicked.connect(self.browseFiles2)
        
        # Go
        self.goButton = QtGui.QPushButton(self.frame)
        self.goButton.setText('Begin merge\n(may take a minute)')
        self.goButton.setGeometry(300,400,200,100)
        self.goButton.clicked.connect(self.go)
        
        self.frame.show()

    # File browsing dialogs. Return string of .ser file.
    # Could not figure out how to update paths with a return function and thus had to make
    # two separate functions
    def browseFiles(self):
        fileName = QtGui.QFileDialog.getOpenFileName(self,
    "Load Series", "/home/", "Series File (*.ser)")
        self.s1path = str(fileName[0])
        self.s1Button.setText(self.s1path.rpartition('/')[2])
    def browseFiles2(self):
        fileName = QtGui.QFileDialog.getOpenFileName(self,
    "Load Series", "/home/", "Series File (*.ser)")
        self.s2path = str(fileName[0])
        self.s2Button.setText(self.s2path.rpartition('/')[2])
        
    def go(self):
        print('s1path: '+str(self.s1path))
        print('s2path: '+str(self.s2path))
        if '.ser' in str(self.s1path) and '.ser' in str(self.s2path):
            print('Beginning merge...') # === popup window
            self.frame.hide()
            seriesAttributes(self.parent, self.s1path, self.s2path)
        else:
            error = QtGui.QMessageBox(self)
            error.setText('Please load valid .ser into each slot!')
            error.exec_()
            
class seriesAttributes(QtGui.QWidget):
    def __init__(self, parent=None, s1p=None, s2p=None):
        QtGui.QWidget.__init__(self, parent)
        self.parent = parent
        
        # Frame
        self.frame = QtGui.QFrame(parent)
        self.frame.setGeometry(0,0,800,500)
        
        # Create series objects from paths
        self.ser1 = rmt.getSeries(s1p)
        self.ser2 = rmt.getSeries(s2p)
        
        # Create attribute list for each series
        ser1atts = self.ser1.output()[0]
        ser2atts = self.ser2.output()[0]
        
        # Create 3 column table: left column has name of all attributes,
        # middle column is all ser1 atts, right column is all ser2 atts.
        # Highlight same atts in green for both rows
        # Rest can only be picked from 1 column
        table = QtGui.QTableWidget(len(ser1atts), 2, parent=self.frame)
        table.setGeometry(0,0,800,500)
        table.setHorizontalHeaderLabels([self.ser1.name, self.ser2.name])
        table.setVerticalHeaderLabels([attribute for attribute in self.ser1._attribs])
        # Load table with attributes
        for row in range(len(ser1atts)):
            header = table.verticalHeaderItem(row).text()
            # Series 1
            tableItem = QtGui.QTableWidgetItem( ser1atts[header] )
            table.setItem(row,0,tableItem)
            # Series 2
            tableItem = QtGui.QTableWidgetItem( ser2atts[header] )
            table.setItem(row,1,tableItem)
#         item.isSelected()
#         setBackground(brush)
#         table.setCurrentCell(r,c,comm) # <-- use to pick only 1 at a time
#         table.selectedItems()
        self.frame.show()
        
        
        
        
        
         

        
def main():
    app = QtGui.QApplication(sys.argv)
    win = mainFrame()
    welcomeButton(win) # begin chain of rmtgui stuff
    sys.exit( app.exec_() )

if __name__ == '__main__':
    main()