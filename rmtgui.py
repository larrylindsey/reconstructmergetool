from PySide import QtGui, QtCore
import reconstructmergetool as rmt
import sys

class mainFrame(QtGui.QFrame):
    '''The mainFrame() class holds all the contents of the reconstructmergetool (RMT) gui. It is the one
    RMTgui class that is open throughout the entire program.
    GUI-wise: the mainframe contains the widgets necessary for proper functioning of RMT. And a
        quit button.
    Data-wise: It contains all the important info regarding the series that are being merged.'''
    def __init__(self, parent=None):
        QtGui.QFrame.__init__(self, parent)
        self.initUI()
        
        # Data
        self.ser1path = None
        self.ser2path = None
        self.ser1obj = None
        self.ser2obj = None
        self.mergedSer = None
        
    def initUI(self):
        # Quit Button
        quitButton = QtGui.QPushButton(self)
        quitButton.setText('Quit')
        quitButton.clicked.connect( QtCore.QCoreApplication.instance().quit )
        
        # Window Dimensions and Attributes
        self.setGeometry(0,0,800,600)
        self.setWindowTitle('Reconstructmergetool v.1')
        self.setFrameStyle(QtGui.QFrame.Box | QtGui.QFrame.Plain)
        self.setLineWidth(2)
        self.setMidLineWidth(3)
        
        # Layout
        hbox = QtGui.QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(quitButton)
        vbox = QtGui.QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox)
        self.setLayout(vbox)

        self.show()

class serLoadWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.initUI()
        # Data
        self.parent = parent
        self.s1p = None
        self.s2p = None
        
    def initUI(self):
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        self.setGeometry(0,0,800,500)
        
        # Load Series Buttons
        self.ser1Button = QtGui.QPushButton('Load Series 1', parent=self)
        self.ser1Button.setGeometry(400-150,100,300,100)
        self.ser1Button.clicked.connect( self.loadSeries )
        
        self.ser2Button = QtGui.QPushButton('Load Series 2', parent=self)
        self.ser2Button.setGeometry(400-150,250,300,100)
        self.ser2Button.clicked.connect( self.loadSeries )
        
        # Continue button
        self.continueButton = QtGui.QPushButton(self)
        self.continueButton.setText('Load both series\nto continue')
        self.continueButton.setGeometry(400-75,400,150,75)
        self.continueButton.setFlat(True)
        
        self.show()
        
    def loadSeries(self):
        fileName = QtGui.QFileDialog.getOpenFileName(self,
                                                     "Load Series",
                                                     "/home/",
                                                     "Series File (*.ser)")
        # Change appropriate path
        if self.sender() == self.ser1Button:
            self.s1p=str(fileName[0])
            self.parent.ser1path = self.s1p
            self.parent.ser1obj = rmt.getSeries(self.s1p)
            self.ser1Button.setText(self.s1p.rsplit('/')[len(self.s1p.split('/'))-1]) # Text = ser name
            self.ser1Button.setFlat(True)
        elif self.sender() == self.ser2Button:
            self.s2p=str(fileName[0])
            self.ser2Button.setText(self.s2p.rsplit('/')[len(self.s2p.split('/'))-1])
            self.ser2Button.setFlat(True)
            self.parent.ser2path = self.s2p
            self.parent.ser2obj = rmt.getSeries(self.s2p)

        # Check to see if both series are loaded
        if self.s1p != None and self.s2p != None:
            self.continueButton.show()
            self.continueButton.setText('Continue...')
            self.continueButton.setFlat(False)
            self.continueButton.clicked.connect( self.nextStep )
            
    def nextStep(self):
        '''Updates data in the mainFrame() class'''
        serAttributeWidget(self.parent)
        self.close()
        
class serAttributeWidget(QtGui.QWidget): #=== problems getting table loaded
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        # Data
        self.parent = parent
        self.ser1obj = parent.ser1obj
        self.ser2obj = parent.ser2obj
        self.ser3obj = None
        self.initUI()
        
    def initUI(self):
        message = QtGui.QMessageBox(self)
        message.setText('Please be patient...\nThis process may take a few minutes.')
        message.show()
        self.table = serAttributeTable(self,
                                       s1atts=self.ser1obj.output()[0],
                                       s2atts=self.ser2obj.output()[0])
        self.table.show()
        print('should be up')

class serAttributeTable(QtGui.QTableWidget):
    '''Receives a parent frame, series1 attributes and series2 attributes. Provides a table display
    GUI for selecting and outputting the attributes to be included in the merged series'''
    def __init__(self, parent=None, s1atts=None, s2atts=None):
        QtGui.QTableWidget.__init__(self, len(s1atts), 2, parent=parent)
        self.parent = parent
        self.ser1 = self.parent.ser1obj
        self.ser2 = self.parent.ser2obj
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
def main():
    app = QtGui.QApplication(sys.argv)
    rmtFrame = mainFrame()
    serLoadWidget( rmtFrame )
    sys.exit( app.exec_() )
main()