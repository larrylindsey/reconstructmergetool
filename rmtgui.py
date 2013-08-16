#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import reconstructmergetool as rmt
from PySide import QtCore, QtGui

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
        self.rmtStart()
         
    def rmtStart(self): #===
        '''This function begins the process of merging series'''
        welcomeButton(self)
        
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

class seriesAttributeTable(QtGui.QTableWidget):
    '''Receives a parent frame, series1 attributes and series2 attributes. Provides a table display
    GUI for selecting and outputting the attributes to be included in the merged series'''
    def __init__(self, parent=None, s1atts=None, s2atts=None):
        QtGui.QTableWidget.__init__(self, len(s1atts), 2, parent=parent)
        self.parent = parent
        
        # Create table
        self.setColumnWidth(0, 318)
        self.setColumnWidth(1, 318)
        self.setGeometry(0,0,800,500)
        
        # Make attribute labels for rows, series names for columns
        self.setHorizontalHeaderLabels( [self.ser1.name, self.ser2.name] ) #==== namess
        self.setVerticalHeaderLabels( [attribute for attribute in self.ser1._attribs] )
        
        # Some rows need to be taller to show all output
        self.setWordWrap(True)
        self.resizeRowsToContents()
        self.setRowHeight(55, 100) # borderColors
        self.setRowHeight(56, 100) # fillcolors
        self.setRowHeight(83, 75) # mvmtIncrement
        self.setRowHeight(84, 75) # ctrlIncrement
        self.setRowHeight(85, 75) # shiftIncrement
        
        # Load table with attributes
        for row in range(len(s1atts)):
            header = self.verticalHeaderItem(row).text()
            # Series 1
            tableItem = QtGui.QTableWidgetItem( s1atts[header] )
            self.setItem(row,0,tableItem)
            # Series 2
            tableItem = QtGui.QTableWidgetItem( s2atts[header] )
            self.setItem(row,1,tableItem)
        
        self.show()
        
    def returnItems(self):
        return self.selectedItems()
        
class seriesAttributes(QtGui.QWidget):
    def __init__(self, parent=None, s1p=None, s2p=None):
        QtGui.QWidget.__init__(self, parent)
        self.parent = parent
        
        # Frame
        self.frame = QtGui.QFrame(parent)
        self.frame.setGeometry(0,0,800,500)
        #=== question mark box with instructions?
        #=== merge button
        
        # Create series objects from paths
        self.ser1 = rmt.getSeries(s1p)
        self.ser2 = rmt.getSeries(s2p)
        
        # Create attribute list for each series
        ser1atts = self.ser1.output()[0]
        ser2atts = self.ser2.output()[0]
        
        # Create table
        self.table = seriesAttributeTable(parent=parent, s1atts=ser1atts, s2atts=ser2atts)
        
        # Output
        self.goButton = QtGui.QPushButton(parent)
        self.goButton.setText('Continue')
        self.goButton.setGeometry(300,500,200,100)
        self.goButton.clicked.connect(self.go)
        
        self.goButton.show()
        self.frame.show()
        
    def go(self):
        items = self.table.selectedItems()
        if len(items) == 86:
            print('Output Series Attributes')
            self.goButton.hide()
            self.frame.hide()
            for item in items:
                print(item.type)
        else:
            error = QtGui.QMessageBox(self)
            error.setText('Make sure attributes are selected: 1 per row')
            error.exec_()
def main():
    app = QtGui.QApplication(sys.argv)
    win = mainFrame()
#     welcomeButton(win) # begin chain of rmtgui stuff
    sys.exit( app.exec_() )

if __name__ == '__main__':
    main()